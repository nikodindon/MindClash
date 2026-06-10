# EP003 — Jancovici vs Lovins: The Debate

> **Status**: design phase, framework to be implemented
> **Planned release**: after EP002 (Lovins solo), summer 2026
> **Format**: debate, English, **~1h target** (vs ~25 min for the solo pods)
> **Format inspiration**: nikodindon/Arena (4-tour debate structure: plaidoyer,
> réfutation, question, conclusion) + a moderator
> **Voice casting** (Kokoro): Alex=`am_adam`, Marc=`am_michael` for the
> 2 debaters (channel continuity), Bella=`af_bella` for the moderator

## Strategic context

This is the **third MindClash episode** and the first debate. The channel
arc:
- **EP001** (Jancovici solo) — sets up the thermodynamic pessimist view
- **EP002** (Lovins solo) — sets up the soft energy / efficiency optimist view
- **EP003** (this one) — puts them in the ring

By the time listeners get here, they've already spent ~40 min with each
persona's voice and thinking. The debate can dive in faster than a cold-start
debate would.

## Topic

> **Is nuclear the only viable path to carbon neutrality by 2050?**
> (Or, by extension: is the energy transition a problem of *production*
> [Jancovici] or a problem of *waste* [Lovins]?)

## Format (4 tours, Arena-inspired)

| Tour | A (Jancovici) | B (Lovins) | Moderator |
|------|---------------|------------|-----------|
| 1 — Plaidoyer | 5 min: opening thesis | 5 min: opening thesis | 1 min: setup |
| 2 — Réfutation | 4 min: attack B's opening | 4 min: attack A's opening | 1 min: scoring |
| 3 — Question | 2 min: trap question for B | 2 min: trap question for A | 2 min: receive answers |
| 4 — Conclusion | 4 min: final position | 4 min: final position | 2 min: verdict |

**Total**: ~30 min speaking time + ~5 min intro/outro + musical beds ≈ **~1h
target as requested**.

The debate will use a real-time scoring system (Arena-inspired: 0-3 points
per camp per tour) and produce a final verdict. A summary paragraph will
note where the two visions actually **converge** (rare, but exists — both
agree on the need to reduce fossil dependence) and where they **fundamentally
disagree** (intermittency vs dispatchability, efficiency vs scale, soft paths
vs big engineering).

## Voice casting (Kokoro TTS)

| Role | Voice | Reason |
|------|-------|--------|
| **Jancovici** (debater A) | `am_adam` (US male) | Alex's voice, but pitched/declaimed more seriously for the French engineer |
| **Lovins** (debater B) | `am_michael` (US male) | Marc's voice, more optimistic and faster cadence |
| **Moderator** (third voice) | `af_bella` (US female) | Distinct from the 2 male debaters; reads as impartial host |

Why `af_bella` and not a male voice? Because both debaters are male, a
female moderator gives a clear visual/auditory separation. The female
voice also reads as more "neutral referee" in English-language debate
tradition (e.g. NPR, NYT podcast moderation).

## `script.json` schema (planned)

Mirroring EP001/EP002, with debate-specific fields:

```json
{
  "episode": "EP003",
  "title": "...",
  "title_fr": "...",
  "duration_target_seconds": 3600,
  "language": "en",
  "format": "debate_cast",
  "speakers": {
    "debater_a": "Jancovici (am_adam)",
    "debater_b": "Lovins (am_michael)",
    "moderator": "Bella (af_bella)"
  },
  "sources": [
    "knowledge_base/science/jancovici/_profile.md",
    "knowledge_base/science/jancovici/lectures/...",
    "knowledge_base/science/lovins/_profile.md",
    "knowledge_base/science/lovins/lectures/..."
  ],
  "tours": [
    {
      "id": 1,
      "name": "plaidoyer",
      "topic": "Opening thesis",
      "segments": [
        {"id": 1, "tour": 1, "speaker": "moderator", "text": "...", "emotion": "...", "pause_after_ms": 600},
        {"id": 2, "tour": 1, "speaker": "debater_a", "text": "...", "emotion": "...", "pause_after_ms": 800},
        ...
      ],
      "scoring": {"debater_a": 0, "debater_b": 0, "rationale": "TBD"}
    },
    ...
  ],
  "final_verdict": {
    "winner": "...",
    "score_a": 0,
    "score_b": 0,
    "verdict_text": "..."
  },
  "post_production_notes": {...}
}
```

**Key differences vs solo EP**:
- 3 voices instead of 2 (need Kokoro to load 3 voice embeddings)
- Segments are grouped by `tour` (4 tours), not by `section` (7 sections)
- Each tour has a `scoring` block with 0-3 per camp + rationale
- Final `verdict` block at the end (winner + summary)
- Total ~150-200 segments (vs 64 for solo, because of 1h runtime and 3 voices)

## Files

| File | Description | Status |
|------|-------------|--------|
| `README.md` | This file | ✅ |
| `show_notes.md` | YouTube description + timestamps | ⏳ template, fill after script |
| `debate_raw.json` | Arena-style debate output (4 tours + scores) | ⏳ |
| `script.json` | Podcast script (segmented, ~150-200 segs) | ⏳ |
| `audio_segments/` | Individual TTS segments | ⏳ |
| `master.wav` | Master audio | ⏳ |
| `final.wav` / `final.mp3` | Mixed with intro/outro music | ⏳ |
| `video.mp4` | YouTube-ready video | ⏳ |

## KB sources

- **Jancovici**: see `knowledge_base/science/jancovici/_profile.md` +
  `knowledge_base/science/jancovici/lectures/` (8 cours Mines 2019)
- **Lovins**: see `knowledge_base/science/lovins/_profile.md` +
  `knowledge_base/science/lovins/lectures/` (4 talks, June 2026)

Both `_profile.md` files are aligned structurally (Bio, Thesis, Thèses,
Concepts, **Red lines**, Citations) — so feeding them to an LLM for
debate generation should be straightforward.

## Production pipeline (TBD)

To be designed after EP002 ships. Three subtasks:
1. **Debate generator script** (analog to `generate_lovins_script.py` but
   calls Qwen with both `_profile.md` files and a 4-tour prompt).
2. **TTS renderer** (analog to `produce_ep002.py` but with 3 voices mapped:
   `am_adam` for A, `am_michael` for B, `af_bella` for moderator).
3. **Mix + video** (analog to `mix_ep002.py` + `render_video_ep002.py`).

## Estimated total time

For a 1h debate with 3 voices:
- Debate script generation: ~1h via Qwen (4 tours × 1 call each, larger prompts)
- TTS rendering: ~15-20 min on GPU (more segments than EP002)
- Mix + video: <2 min
- **Total: ~1.5-2h from green light to final video**

## Production checklist

- [ ] Voice casting finalized (af_bella confirmed?)
- [ ] Write the debate generator script (4-tour prompt, both KBs)
- [ ] Generate the 4 tours (~150-200 segments total)
- [ ] Score each tour (Arena-style 0-3 per camp)
- [ ] Generate the final verdict
- [ ] Render TTS (3 voices × N segments)
- [ ] Mix intro/outro music + transition stings between tours
- [ ] Render video with the EP003 background (to be designed)
- [ ] Verify all 4 tours + verdict segments in the final audio
- [ ] Update show_notes.md with real timestamps + per-tour summaries
