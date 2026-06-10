# EP003 — Jancovici vs Lovins: The Debate

> **Status**: seed (renamed from EP001_jancovici-vs-lovins on 2026-06-10)
> **Planned release**: after EP002 (Lovins solo), summer 2026
> **Format**: debate, English, **~1h target** (vs ~25 min for the solo pods)
> **Format inspiration**: nikodindon/Arena (4-tour debate structure: plaidoyer,
> réfutation, question, conclusion) + a moderator

## Strategic context

This is the **third MindClash episode** and the first debate. The channel
arc:
- **EP001** (Jancovici solo) — sets up the thermodynamic pessimist view
- **EP002** (Lovins solo) — sets up the soft energy / efficiency optimist view
- **EP003** (this one) — puts them in the ring

By the time listeners get here, they've already spent 45 min with each
persona's voice and thinking. The debate can dive in faster than a cold-start
debate would.

## Persons

- **Debater A** (Jancovici voice, Marc-style): the high-priest of energy
  realism — civilization as a thermodynamic system, peak oil as geology,
  nuclear as a necessary bridge.
- **Debater B** (Lovins voice, Alex-style): the soft-energy heretic —
  negawatts, design integratif, Reinventing Fire, "efficiency is 10× cheaper
  than nuclear per ton of CO₂".
- **Moderator** (third voice): keeps score, asks the trap question, ensures
  both sides get fair airtime.

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

## Files

| File | Description | Status |
|------|-------------|--------|
| `README.md` | This file | ✅ |
| `show_notes.md` | YouTube description + timestamps | ⏳ template, fill after script |
| `debate_raw.json` | Arena-style debate output (4 tours + scores) | ⏳ |
| `script.json` | Podcast script (segmented) | ⏳ |
| `audio_segments/` | Individual TTS segments | ⏳ |
| `master.wav` | Master audio | ⏳ |
| `final.wav` / `final.mp3` | Mixed with intro/outro music | ⏳ |
| `video.mp4` | YouTube-ready video | ⏳ |

## KB sources

- **Jancovici**: see `knowledge_base/science/jancovici/_profile.md` +
  `knowledge_base/science/jancovici/lectures/` (8 cours Mines 2019)
- **Lovins**: see `knowledge_base/science/lovins/_profile.md` +
  `knowledge_base/science/lovins/lectures/` (4 talks, June 2026)

## Production pipeline (TBD)

To be designed after EP002 ships. The Arena format (4 tours + moderator +
score) will likely be re-implemented as a dedicated script. Three voices
mean we'll need 6 voices from Kokoro:
- Jancovici = ? (currently Alex=am_adam, but we may want a deeper voice for
  a French engineer)
- Lovins = ? (currently Marc=am_michael)
- Moderator = af_bella or bf_emma (one of the female Kokoro voices)

## Production checklist

- [ ] Decide voice casting for the 3 roles
- [ ] Write a debate generator script (Arena-inspired, MindClash-flavored)
- [ ] Generate the 4-tour debate from the two `_profile.md` files
- [ ] Run the script
- [ ] Render TTS (3 voices × N segments)
- [ ] Mix intro/outro music + transition stings between tours
- [ ] Render video
- [ ] Add "verdict" segment in the show notes
