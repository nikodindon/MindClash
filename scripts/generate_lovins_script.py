#!/usr/bin/env python3
"""
Generate EP002 Lovins-solo podcast script.json via Qwen distant.

Calls Qwen 7 times (one per section), then assembles all segments into
a single script.json that mirrors the EP001 structure exactly.

Usage: python3 scripts/generate_lovins_script.py
"""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path('/home/niko/MindClash')
OUT = ROOT / 'episodes/EP002_lovins-synthesis/script.json'
PROFILE = ROOT / 'knowledge_base/science/lovins/_profile.md'

QWEN_URL = "http://100.118.85.70:8080/v1/chat/completions"

# Sections config — (name, num_segments, topic_summary)
SECTIONS = [
    ("intro", 5,
     "Welcome to MindClash EP002 on Amory Lovins. Host Alex introduces the "
     "episode, says who Lovins is (RMI founder, 50 years of soft energy, "
     "coined the term negawatt). Then hands off to expert Marc, who explains "
     "what first hit him when going through the 4 talks. Alex frames the "
     "episode as the optimistic counterweight to Jancovici (EP001)."),
    ("fifth-option", 10,
     "The 'fifth option' thesis: instead of choosing between oil wars, "
     "climate change, nuclear holocaust, or declining living standards, "
     "there is a 5th option — none of the above. Negawatts, efficiency, "
     "Reinventing Fire. The 5000 billion dollars saved. The Empire State "
     "Building example. The 'obstacles are cultural not technical' framing."),
    ("reinventing-fire", 12,
     "Deep dive on the Reinventing Fire programme. The 4 sectors "
     "(buildings, transport, electricity, industry). The 2-4% per year "
     "energy intensity reduction that already happened historically in the "
     "US, and 5% per year in China. The 2/5 of US coal electricity that "
     "could be displaced by industrial cogeneration. Eliminating US oil "
     "use by the 2040s. The 'doing more with less' framing."),
    ("design-integratif", 11,
     "Design integratif: optimize the system, not the components. The 40 "
     "000+ passive buildings in Europe. The Empire State Building -70% "
     "energy renovation. RMI's office as one of the most efficient in "
     "North America. Making heating/cooling equipment unnecessary through "
     "building envelope. Amsterdam social housing as energy producers. "
     "Texas and California grids running on massive solar + batteries."),
    ("soft-energy", 10,
     "Soft energy paths: the 1976 manifesto. Decentralized, renewable, "
     "appropriable sources. The critique of nuclear: more expensive, "
     "slower to build, in relative decline. The 'efficiency is 10x cheaper "
     "than nuclear per ton of CO2'. The microgrid resilience argument. "
     "Why Lovins calls nuclear an 'old boys' network of subsidies'."),
    ("critique", 12,
     "The honest critique section. The red lines from the self-critique: "
     "(1) overestimating microgrid resilience vs supply chain risks and "
     "cyberwarfare, (2) minimizing mining impacts of lithium/cobalt/copper "
     "for green tech, (3) over-optimistic on AI energy demand and optical "
     "chips, (4) disconnect between local economic viability and global "
     "political realities (subsidies, sovereignty), (5) reductionism of "
     "social complexity via individualist 'applied hope' framing. The "
     "two open questions for the EP003 debate."),
    ("outro", 4,
     "Wrap-up. Marc's final verdict on Lovins: brilliant system thinker, "
     "visionary, but optimism gets thin on global politics. Alex teases "
     "EP003: 'Jancovici vs Lovins — the debate'. 1h, three voices, two "
     "visions head-to-head. Subscribe prompt. Sign-off."),
]

SPEAKERS = {"host": "Alex (am_adam)", "expert": "Marc (am_michael)"}

# Read the Lovins profile to inject as context
profile_text = PROFILE.read_text(encoding="utf-8")

# Truncate profile to keep prompt size manageable
if len(profile_text) > 12000:
    profile_text = profile_text[:12000] + "\n\n[... truncated for context window ...]"


def call_qwen(prompt: str, max_tokens: int = 4000) -> str:
    """Call Qwen distant with thinking disabled."""
    payload = {
        "model": "qwen3",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(
        QWEN_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        body = json.loads(r.read())
    return body["choices"][0]["message"]["content"]


def make_prompt(section_name: str, num_segments: int, topic_summary: str,
                prev_segments: list) -> str:
    """Build a section-specific prompt with cumulative context."""
    prev_text = ""
    if prev_segments:
        prev_text = f"\n\n## PREVIOUS SEGMENTS (so far, for continuity):\n"
        for s in prev_segments[-10:]:  # last 10 for context window
            prev_text += f"  #{s['id']} [{s['section']:18s}] {s['speaker']:6s} ({s.get('emotion','?')}): {s['text']}\n"

    prompt = f"""Tu génères la section '{section_name}' d'un podcast MindClash EP002 sur Amory Lovins.

## Section à produire : {section_name} ({num_segments} segments)

**Sujet** : {topic_summary}

## Speakers

- host = Alex (am_adam, US male, deeper voice) — pose les questions, anime
- expert = Marc (am_michael, US male) — répond, explique, analyse

## Format de chaque segment (OBLIGATOIRE)

Un objet JSON avec exactement ces clés :
- "id" (int, continue la numérotation depuis le dernier segment précédent)
- "section" (string, toujours "{section_name}")
- "speaker" (string, "host" ou "expert")
- "text" (string, 40-80 mots, 1-3 phrases parlées, anglais naturel conversationnel)
- "emotion" (string parmi : friendly, engaged, curious, thoughtful, serious, balanced, passionate, informing, skeptical, amused, warm, incredulous, insightful, matter-of-fact, enthusiastic, informative)
- "pause_after_ms" (int, 300-1500)

## KB de Lovins (extrait)

{profile_text}
{prev_text}

## Consignes

1. Anglais naturel conversationnel, comme un vrai podcast
2. Citer au moins 1 fait précis Lovins par segment (chiffre, exemple, citation)
3. Varier les émotions (ne pas répéter "thoughtful" 5 fois d'affilée)
4. L'host pose des questions, l'expert répond — sauf cas narratif
5. Sortie UNIQUEMENT un array JSON valide, sans préambule, sans ```json```, sans commentaires
6. Commence directement par `[{{"id": ..., "section": "{section_name}", ...`

Génère EXACTEMENT {num_segments} segments pour cette section.
"""
    return prompt


def parse_json_array(text: str) -> list:
    """Parse a JSON array from model output, robust to markdown fences."""
    text = text.strip()
    # Strip markdown fences
    if text.startswith("```"):
        # Remove opening fence (could be ```json or ```)
        first_newline = text.find("\n")
        text = text[first_newline + 1:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    return json.loads(text)


def main():
    all_segments = []
    next_id = 1

    for i, (section_name, num_segments, topic_summary) in enumerate(SECTIONS):
        print(f"\n[{time.strftime('%H:%M:%S')}] === Section {i+1}/7 : {section_name} ({num_segments} segments) ===", flush=True)
        prompt = make_prompt(section_name, num_segments, topic_summary, all_segments)
        print(f"  prompt size: {len(prompt)} chars", flush=True)

        t0 = time.time()
        raw = call_qwen(prompt, max_tokens=4000)
        elapsed = time.time() - t0
        print(f"  Qwen: {elapsed:.1f}s, {len(raw)} chars", flush=True)

        try:
            segs = parse_json_array(raw)
        except json.JSONDecodeError as e:
            print(f"  JSON parse error: {e}", flush=True)
            print(f"  raw (first 500): {raw[:500]}", flush=True)
            print(f"  raw (last 500):  {raw[-500:]}", flush=True)
            raise

        # Renumber segments to ensure continuous IDs
        for j, s in enumerate(segs):
            s['id'] = next_id + j
            s['section'] = section_name
            if 'pause_after_ms' not in s:
                s['pause_after_ms'] = 700
        next_id += len(segs)

        all_segments.extend(segs)
        print(f"  parsed {len(segs)} segments (total: {len(all_segments)})", flush=True)

    # Assemble final script.json
    script = {
        "episode": "EP002",
        "title": "The Negawatt Revolution: What Amory Lovins Actually Proposes",
        "title_fr": "La révolution negawatt : ce que propose vraiment Amory Lovins",
        "duration_target_seconds": 1450,
        "language": "en",
        "format": "interview",
        "speakers": SPEAKERS,
        "sources": [
            "knowledge_base/science/lovins/_profile.md",
            "knowledge_base/science/lovins/lectures/40-year-plan-energy-2026-06-10.md",
            "knowledge_base/science/lovins/lectures/reinventing-fire-2026-06-10.md",
            "knowledge_base/science/lovins/lectures/applied-hope-tedx-2026-06-10.md",
            "knowledge_base/science/lovins/lectures/rmi-co-founder-talk-2026-06-10.md",
        ],
        "segments": all_segments,
        "post_production_notes": {
            "music_intro": "8-12 sec ambient bed, fade in",
            "music_outro": "8-12 sec ambient bed, fade out with EP003 teaser",
            "music_transitions": "subtle 1-2 sec whoosh between sections",
            "sfx": "optional soft chime at end of intro and start of outro",
            "background_image_for_video": "episodes/EP002_lovins-synthesis/background.png (THE NEGAWATT REVOLUTION + 'A podcast on Amory Lovins' subtitle)"
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(script, ensure_ascii=False, indent=2))
    print(f"\n[OK] Wrote {OUT}", flush=True)
    print(f"  Total segments: {len(all_segments)}", flush=True)
    print(f"  Sections: {dict((s, sum(1 for x in all_segments if x['section']==s)) for s in [n for n,_,_ in SECTIONS])}", flush=True)
    print(f"  Speakers: host={sum(1 for s in all_segments if s['speaker']=='host')}, expert={sum(1 for s in all_segments if s['speaker']=='expert')}", flush=True)


if __name__ == "__main__":
    main()
