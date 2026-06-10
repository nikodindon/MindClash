#!/usr/bin/env python3
"""
Generate EP003 Jancovici-vs-Lovins debate script.json via Qwen distant.

Calls Qwen 5 times (4 tours + 1 verdict), then assembles all segments
into a single script.json following the debate_cast schema.

Format: 3 voices (debater_a = Jancovici, debater_b = Lovins, moderator
= Bella), 4 Arena-inspired tours (plaidoyer / réfutation / question /
conclusion), final verdict.

Usage: python3 scripts/generate_debate_ep003.py
"""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path('/home/niko/MindClash')
OUT_SCRIPT = ROOT / 'episodes/EP003_jancovici-vs-lovins/script.json'
OUT_RAW = ROOT / 'episodes/EP003_jancovici-vs-lovins/debate_raw.json'

PROFILE_J = ROOT / 'knowledge_base/science/jancovici/_profile.md'
PROFILE_L = ROOT / 'knowledge_base/science/lovins/_profile.md'

QWEN_URL = "http://100.118.85.70:8080/v1/chat/completions"

# Topic
TOPIC = "Is nuclear the only viable path to carbon neutrality by 2050?"

# Tours config — (id, name, num_segments, instructions)
TOURS = [
    (1, "plaidoyer", 12,
     "Each debater presents their opening thesis. Jancovici (debater_a) "
     "opens with the production-side argument: civilization is a thermodynamic "
     "system, scale matters, nuclear is the only proven dispatchable low-carbon "
     "source that can replace fossil baseload at scale. Lovins (debater_b) "
     "follows with the waste-side argument: 4/5 of energy is wasted through "
     "inefficient design, negawatts + design integratif + renewables can do "
     "the job at lower cost. The moderator opens the tour, then each debater "
     "speaks for ~5 minutes total. No attacks yet — just position-setting."),

    (2, "refutation", 14,
     "Each debater attacks the other's opening thesis. Jancovici attacks "
     "Lovins's optimism: intermittency of renewables, the baseload problem, "
     "the hidden costs of storage, the realism of building 40,000+ retrofits. "
     "Lovins attacks Jancovici's nuclear enthusiasm: cost overruns (Vogtle, "
     "Hinkley Point, Olkiluoto), the 10-15 year build time, the stranded "
     "asset risk, the 'efficiency is 10x cheaper per ton of CO2' argument. "
     "Moderator scores 0-3 per camp at the end of this tour."),

    (3, "question", 10,
     "Each debater poses a trap question to the other. Jancovici asks: "
     "'If renewables + efficiency are so cheap, why has the US installed "
     "more nuclear capacity than solar in the last 5 years?' Lovins asks: "
     "'If nuclear is necessary, why is China — your model of state-led "
     "industrial policy — building twice as much solar + wind as nuclear?' "
     "Then each debater has 1-2 minutes to respond. Moderator notes who "
     "answered better. Scoring at end of tour."),

    (4, "conclusion", 10,
     "Each debater delivers a 4-minute final position. No new arguments — "
     "just the strongest version of their case. Jancovici concludes: nuclear "
     "is necessary, not sufficient — we also need renewables and efficiency, "
     "but the dispatchability question is real. Lovins concludes: nuclear is "
     "not necessary, the market is voting with its dollars, and the only "
     "honest path is through efficiency + renewables + grids. Moderator "
     "renders a final verdict at the end, noting both score and rare points "
     "of convergence."),
]

# Outro after the verdict (teaser for next)
OUTRO_SEGMENTS = 4

SPEAKERS = {
    "debater_a": "Jancovici (am_adam)",
    "debater_b": "Lovins (am_michael)",
    "moderator": "Bella (af_bella)",
}

# Voice mapping for TTS
VOICE_MAP = {
    "debater_a": "am_adam",
    "debater_b": "am_michael",
    "moderator": "af_bella",
}

# Read both profiles
profile_j = PROFILE_J.read_text(encoding="utf-8")
profile_l = PROFILE_L.read_text(encoding="utf-8")


def extract_compact_profile(text: str) -> str:
    """Extract only the key sections (thesis + theses + concepts + red lines)
    to keep prompts small. Skip the bio and verbose sections."""
    import re
    out_lines = []
    current_section = ""
    keep_sections = {"Thèse centrale", "thèses structurantes", "Concepts signature",
                     "Red lines", "Questions ouvertes", "Citations verbatim"}
    skip_sections = {"Bio express", "Bio ", "## Bio", "## Sources"}
    for line in text.split("\n"):
        if line.startswith("## "):
            current_section = line
            continue
        out_lines.append(line)

    # Re-parse: only keep content under keep_sections
    result = []
    in_keep = False
    for line in text.split("\n"):
        if line.startswith("## "):
            in_keep = any(k in line for k in keep_sections)
            if in_keep:
                result.append(line)
        elif in_keep:
            result.append(line)

    compact = "\n".join(result)
    # Final cap
    if len(compact) > 4000:
        compact = compact[:4000] + "\n\n[... truncated ...]"
    return compact


profile_j_compact = extract_compact_profile(profile_j)
profile_l_compact = extract_compact_profile(profile_l)
print(f"Compact profiles: J={len(profile_j_compact)} chars, L={len(profile_l_compact)} chars")


def call_qwen(prompt: str, max_tokens: int = 4500) -> str:
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
    with urllib.request.urlopen(req, timeout=900) as r:
        body = json.loads(r.read())
    return body["choices"][0]["message"]["content"]


def parse_json_array(text: str) -> list:
    """Parse a JSON array from model output, robust to markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        first_newline = text.find("\n")
        text = text[first_newline + 1:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())


def make_tour_prompt(tour_id: int, tour_name: str, num_segments: int,
                     instructions: str, prev_segments: list) -> str:
    """Build a tour-specific prompt with cumulative context."""
    # Last 15 segments for context (smaller than solo because 3 voices = denser)
    prev_text = ""
    if prev_segments:
        prev_text = "\n\n## PREVIOUS SEGMENTS (for continuity):\n"
        for s in prev_segments[-15:]:
            sp = s.get('speaker', '?')
            txt = s.get('text', '')[:100]
            prev_text += f"  #{s['id']} [tour {s.get('tour', '?')}/{s.get('tour_name', '?')}] {sp:12s}: {txt}...\n"

    prompt = f"""Tu génères le Tour {tour_id} ({tour_name}) d'un débat MindClash EP003.

## Contexte

Débat MindClash EP003 : "{TOPIC}"

**3 voix** :
- debater_a = Jancovici (am_adam, US male, French mining engineer) — défend la position "nucléaire nécessaire"
- debater_b = Lovins (am_michael, US male, RMI founder) — défend la position "efficacité + renouvelables suffisent"
- moderator = Bella (af_bella, US female, modératrice neutre)

**Règle** : la modératrice NE PREND PAS PART au débat. Elle ne fait qu'introduire les tours, poser les questions de l'audience, et scorer.

## Tour {tour_id} : {tour_name} — {num_segments} segments à produire

**Instructions** : {instructions}

## KB — Jancovici (extrait)

{profile_j_compact}

## KB — Lovins (extrait)

{profile_l_compact}
{prev_text}

## Format de chaque segment (OBLIGATOIRE)

Objet JSON avec exactement ces clés :
- "id" (int, continue la numérotation depuis le dernier segment précédent)
- "tour" (int, = {tour_id})
- "tour_name" (string, = "{tour_name}")
- "speaker" (string, "debater_a" | "debater_b" | "moderator")
- "text" (string, 40-90 mots, 1-4 phrases, anglais naturel conversationnel)
- "emotion" (parmi : friendly, engaged, curious, thoughtful, serious, balanced, passionate, informing, skeptical, amused, warm, incredulous, insightful, matter-of-fact, enthusiastic, firm, amused-then-serious)
- "pause_after_ms" (int, 300-1500)

## Consignes

1. Anglais naturel conversationnel, comme un vrai débat TV
2. Citer au moins 1 fait précis par segment (chiffre, exemple, citation Lovins/Jancovici)
3. Varier les émotions — un débat vivant alterne tons
4. Modérateur = présentations/relances/scores UNIQUEMENT, jamais d'avis
5. Les débatteurs se citent/attaquent mutuellement
6. Sortie UNIQUEMENT un array JSON valide, sans préambule, sans ``` fences
7. Commence par `[{{"id": ..., "tour": {tour_id}, "tour_name": "{tour_name}", ...`

Génère EXACTEMENT {num_segments} segments pour ce tour.
"""
    return prompt


def make_verdict_prompt(all_segments: list) -> str:
    """Build the final verdict prompt after all 4 tours are done."""
    # Show all segments but compact (first 200 chars each)
    segs_text = "\n".join(
        f"  #{s['id']} [tour {s.get('tour', '?')}/{s.get('tour_name', '?')}] "
        f"{s.get('speaker', '?'):12s}: {s.get('text', '')[:120]}..."
        for s in all_segments
    )

    return f"""Tu rends le verdict final d'un débat MindClash EP003.

## Contexte

Débat : "{TOPIC}"

Voici tous les segments des 4 tours qui viennent d'avoir lieu (compacted) :

{segs_text}

## Ta tâche

Produis 3 objets JSON dans cet ordre EXACT :

1. **scoring_per_tour** : pour chaque tour (1-4), un score 0-3 par débatteur
   Format : `[{{"tour": 1, "debater_a": 2, "debater_b": 1, "rationale": "..."}}, ...]`

2. **verdict_segments** : 4 segments finaux prononcés par la modératrice Bella
   Format : array de 4 objets JSON avec les clés id/tour/tour_name/speaker/text/emotion/pause_after_ms.
   - Segment 1 : "And that's the end of the four rounds. Let me tally the score."
   - Segment 2 : "The final score is X for Jancovici, Y for Lovins."
   - Segment 3 : "But more importantly, here's what struck me..." (synthèse de convergence)
   - Segment 4 : "Where do they actually agree? Where do they fundamentally disagree?"

3. **outro_segments** : 4 segments prononcés par la modératrice pour la sortie
   Format : array de 4 objets JSON.
   - Segment 1 : "That's it for this debate. Thank you both for your time."
   - Segment 2 : "If you enjoyed this format, subscribe..."
   - Segment 3 : teaser pour EP004 (une autre personnalité à venir)
   - Segment 4 : "See you in the next MindClash."

## Format de sortie

Un objet JSON unique avec exactement ces 3 clés :
```json
{{
  "scoring_per_tour": [...],
  "verdict_segments": [...],
  "outro_segments": [...]
}}
```

Pas de préambule. Pas de ``` fences. Commence directement par `{{`.

## Consignes pour le scoring

- 0 = no argument
- 1 = weak argument
- 2 = solid argument
- 3 = strong with specific cite/number

Sois honnête. Le verdict peut être un match nul (ex: 6-6) si les 2 sont au même niveau.

Pour les 4 verdict_segments et 4 outro_segments, garde le format segment strict (id, tour=5, tour_name="verdict" ou "outro", speaker="moderator", text, emotion, pause_after_ms).
"""


def main():
    all_segments = []
    next_id = 1

    for i, (tour_id, tour_name, num_segments, instructions) in enumerate(TOURS):
        print(f"\n[{time.strftime('%H:%M:%S')}] === Tour {tour_id}/4 : {tour_name} ({num_segments} segments) ===", flush=True)
        prompt = make_tour_prompt(tour_id, tour_name, num_segments, instructions, all_segments)
        print(f"  prompt size: {len(prompt)} chars", flush=True)

        t0 = time.time()
        raw = call_qwen(prompt, max_tokens=4500)
        elapsed = time.time() - t0
        print(f"  Qwen: {elapsed:.1f}s, {len(raw)} chars", flush=True)

        try:
            segs = parse_json_array(raw)
        except json.JSONDecodeError as e:
            print(f"  JSON parse error: {e}", flush=True)
            print(f"  raw (first 500): {raw[:500]}", flush=True)
            print(f"  raw (last 500):  {raw[-500:]}", flush=True)
            raise

        # Renumber and normalize
        for j, s in enumerate(segs):
            s['id'] = next_id + j
            s['tour'] = tour_id
            s['tour_name'] = tour_name
            s.setdefault('pause_after_ms', 800)
        next_id += len(segs)

        all_segments.extend(segs)
        print(f"  parsed {len(segs)} segments (total: {len(all_segments)})", flush=True)

    # === Verdict + Outro ===
    print(f"\n[{time.strftime('%H:%M:%S')}] === Verdict + Outro (final Qwen call) ===", flush=True)
    verdict_prompt = make_verdict_prompt(all_segments)
    print(f"  prompt size: {len(verdict_prompt)} chars", flush=True)
    t0 = time.time()
    raw = call_qwen(verdict_prompt, max_tokens=3000)
    print(f"  Qwen: {time.time()-t0:.1f}s, {len(raw)} chars", flush=True)

    try:
        # Parse the verdict as an object (not array)
        text = raw.strip()
        if text.startswith("```"):
            first_newline = text.find("\n")
            text = text[first_newline + 1:]
        if text.endswith("```"):
            text = text[:-3]
        verdict_obj = json.loads(text.strip())
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}", flush=True)
        print(f"  raw: {raw[:1500]}", flush=True)
        raise

    scoring = verdict_obj.get("scoring_per_tour", [])
    verdict_segs = verdict_obj.get("verdict_segments", [])
    outro_segs = verdict_obj.get("outro_segments", [])

    # Renumber verdict (tour 5) and outro (tour 6)
    for j, s in enumerate(verdict_segs):
        s['id'] = next_id + j
        s['tour'] = 5
        s['tour_name'] = "verdict"
        s['speaker'] = "moderator"
        s.setdefault('pause_after_ms', 800)
    next_id += len(verdict_segs)
    all_segments.extend(verdict_segs)
    print(f"  + {len(verdict_segs)} verdict segments (total: {len(all_segments)})", flush=True)

    for j, s in enumerate(outro_segs):
        s['id'] = next_id + j
        s['tour'] = 6
        s['tour_name'] = "outro"
        s['speaker'] = "moderator"
        s.setdefault('pause_after_ms', 800)
    next_id += len(outro_segs)
    all_segments.extend(outro_segs)
    print(f"  + {len(outro_segs)} outro segments (total: {len(all_segments)})", flush=True)

    # === Assemble script.json ===
    # Compute total score
    score_a = sum(s.get('debater_a', 0) for s in scoring)
    score_b = sum(s.get('debater_b', 0) for s in scoring)
    if score_a > score_b:
        winner = "debater_a"
    elif score_b > score_a:
        winner = "debater_b"
    else:
        winner = "tie"

    script = {
        "episode": "EP003",
        "title": "Jancovici vs Lovins: Can We Skip Nuclear?",
        "title_fr": "Jancovici contre Lovins : peut-on se passer du nucléaire ?",
        "duration_target_seconds": 3600,
        "language": "en",
        "format": "debate_cast",
        "topic": TOPIC,
        "speakers": SPEAKERS,
        "voice_map": VOICE_MAP,
        "sources": [
            "knowledge_base/science/jancovici/_profile.md",
            "knowledge_base/science/lovins/_profile.md",
            "episodes/EP001_jancovici-synthesis/script.json",
            "episodes/EP002_lovins-synthesis/script.json",
        ],
        "tours": [
            {"id": tid, "name": tn, "num_segments_target": ns}
            for tid, tn, ns, _ in TOURS
        ],
        "segments": all_segments,
        "scoring_per_tour": scoring,
        "final_verdict": {
            "winner": winner,
            "score_a": score_a,
            "score_b": score_b,
            "score_a_max": 12,  # 4 tours × 3 max per tour
            "score_b_max": 12,
        },
        "post_production_notes": {
            "music_intro": "8-12 sec ambient bed, fade in",
            "music_outro": "8-12 sec ambient bed, fade out",
            "music_transitions": "subtle 2-3 sec whoosh + soft chime between tours (4 transitions: tour 1→2, 2→3, 3→4, 4→verdict)",
            "sfx": "soft chime at end of each tour's scoring moment",
            "background_image_for_video": "episodes/EP003_jancovici-vs-lovins/background.png (JANCOVICI VS LOVINS + 'The energy debate that matters' subtitle)",
        },
    }

    OUT_SCRIPT.parent.mkdir(parents=True, exist_ok=True)
    OUT_SCRIPT.write_text(json.dumps(script, ensure_ascii=False, indent=2))
    print(f"\n[OK] Wrote {OUT_SCRIPT}", flush=True)
    print(f"  Total segments: {len(all_segments)}", flush=True)
    print(f"  Tours: {dict((s.get('tour_name','?'), sum(1 for x in all_segments if x.get('tour_name')==s.get('tour_name'))) for s in [{'tour_name': tn} for _,tn,_,_ in TOURS])}", flush=True)
    print(f"  Speakers: debater_a={sum(1 for s in all_segments if s['speaker']=='debater_a')}, "
          f"debater_b={sum(1 for s in all_segments if s['speaker']=='debater_b')}, "
          f"moderator={sum(1 for s in all_segments if s['speaker']=='moderator')}", flush=True)
    print(f"  Score: Jancovici={score_a}/12, Lovins={score_b}/12 → winner={winner}", flush=True)

    # Also write the raw arena-style output (just the metadata, no segments)
    raw_obj = {
        "topic": TOPIC,
        "debut": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "score_a": score_a,
        "score_b": score_b,
        "tours": [
            {
                "id": tid,
                "name": tn,
                "instructions": inst,
                "scoring": next((s for s in scoring if s['tour'] == tid), {}),
            }
            for tid, tn, _, inst in TOURS
        ],
        "vainqueur": "Jancovici" if winner == "debater_a" else ("Lovins" if winner == "debater_b" else "tie"),
        "vainqueur_texte": f"Final score: Jancovici {score_a}/12, Lovins {score_b}/12",
        "num_segments": len(all_segments),
    }
    OUT_RAW.write_text(json.dumps(raw_obj, ensure_ascii=False, indent=2))
    print(f"[OK] Wrote {OUT_RAW}", flush=True)


if __name__ == "__main__":
    main()
