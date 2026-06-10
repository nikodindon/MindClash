# EP003 — Jancovici vs Lovins: The Debate

> **Status**: seed (design phase, awaiting debate script generation)
> **Planned release**: after EP002, summer 2026
> **Format**: 3-voice debate, English, ~1h target
> **Format inspiration**: nikodindon/Arena (4-tour debate structure)

## YouTube title (EN)

**Jancovici vs Lovins: Can We Skip Nuclear? The Energy Debate That Matters**

## Thumbnail (concept)

- Jancovici and Lovins face-to-face, split image (left/right)
- B&W for both, with a red-vs-blue subtle tint (Jancovici = warmer/red,
  Lovins = cooler/blue)
- Center divider: a thin orange line (MindClash accent)
- Red banner at bottom: **"WHO'S RIGHT?"**
- Style: same engineering-aesthetic as EP001/EP002 (channel continuity)

## YouTube description

> Two visions of the energy transition, head to head.
>
> In EP001, we explored Jean-Marc Jancovici's thermodynamic pessimism:
> civilization as an energy system in collision with planetary limits.
> In EP002, we met Amory Lovins's soft-energy optimism: we don't need
> more power plants, we need less waste, and efficiency is ten times
> cheaper than nuclear per ton of CO₂ avoided.
>
> Now they meet.
>
> In this 1-hour debate, our two debaters go head-to-head on a single
> question: **is nuclear the only viable path to carbon neutrality by
> 2050?** A moderator scores each round (0-3 per camp) and renders a
> final verdict. We also flag the rare points of convergence — because
> the two agree on more than the headlines suggest.
>
> In this episode:
> - Tour 1 — Plaidoyer : Jancovici's production-side view vs Lovins's
>   waste-side view
> - Tour 2 — Réfutation : each attacks the other's opening thesis
> - Tour 3 — Question : a trap question for each
> - Tour 4 — Conclusion : final positions, last sharp arguments
> - Verdict : who won, and where the two actually agree
>
> 🎙️ Jancovici (Marc) vs Lovins (Alex), moderated by Bella
> 📚 Sources: 8 Jancovici Mines lectures (2019) + 4 Lovins talks (TED, RMI)
> ⚠️ Disclaimer: this podcast is AI-assisted. The content is based on
> each thinker's real lectures, with human-curated citation and analysis.
> The debate format is modeled on nikodindon/Arena (4-tour scoring).

## YouTube chapters (TBD — to fill after script is written)

```
0:00 Intro — Welcome to the first MindClash debate
0:30 Meet the debaters + topic framing
?:?? Tour 1 — Plaidoyer
?:?? Tour 2 — Réfutation
?:?? Tour 3 — Question
?:?? Tour 4 — Conclusion
?:?? Verdict — who won, and where they agree
?:?? Outro — wrap-up + next-episode teaser
```

## Tags (EN, ~20 tags)

```
jancovici, lovins, jancovici vs lovins, mindclash, debate, energy debate,
nuclear, renewable energy, climate change, energy transition,
carbon neutrality, peak oil, negawatt, soft energy paths, design integratif,
reinventing fire, mines paris, rocky mountain institute, ai podcast,
ai debate
```

## Sources (in YouTube description)

**Jancovici** (8 Mines ParisTech lectures, 2019):
1. Lecture 1 — Energy
2. Lecture 2 — Fossil fuels
3. Lecture 3 — Climate change (1)
4. Lecture 4 — Climate change (2)
5. Lecture 5 — Energy savings
6. Lecture 6 — Nuclear
7. Lecture 7 — Renewables
8. Lecture 8 — Carbon accounting

(Full URLs in `knowledge_base/science/jancovici/_profile.md` and
`_index.md`.)

**Lovins** (4 talks):
1. TED — A 40-year plan for energy
2. Reinventing Fire
3. TEDx — Applied Hope
4. RMI keynote — Co-founder / Chief Scientist

(Full URLs in `knowledge_base/science/lovins/_profile.md`.)

## Embedded citations (TBD)

Will be auto-extracted from the 4 tours of the debate script once generated.

## Scoring methodology

Each of the 4 tours is scored 0-3 per camp (Arena-inspired):

| Score | Meaning |
|-------|---------|
| 0 | No argument, or completely off-topic |
| 1 | Weak argument, doesn't engage with the other's position |
| 2 | Solid argument, factual, relevant |
| 3 | Strong argument with a specific cite / number, advances the debate |

A typical debate lands around 5-9 total points per camp across 4 tours
(each tour max 3 per side, so total per side = 0-12).

The verdict at the end will note:
- Winner (by score)
- Where the two fundamentally **disagree** (the meat of the debate)
- Where they actually **converge** (often hidden under the rhetoric)

## Production notes

### Audio

- Engine: **Kokoro TTS** (v0.19 ONNX, 24000 Hz, 16-bit)
- Voices:
  - Jancovici (debater A) = `am_adam` (same as Alex/host in EP001-002)
  - Lovins (debater B) = `am_michael` (same as Marc/expert in EP001-002)
  - Moderator (Bella) = `af_bella` (new voice for the channel)
- Pipeline: ~150-200 segments → audio_segments/ → master.wav →
  final.wav → final.mp3
- 3 voices need careful voice embedding loading (Kokoro supports up
  to 11 voices natively in `voices.bin`, so this is fine)

### Video

- Codec: H.264 video + AAC audio
- Resolution: 1280x720 (720p)
- Duration: ~1h target
- Background: `background.png` with EP003 title + subtitle (to be generated)
- Tour transitions: subtle visual change (e.g. a thin orange bar at
  the top of the screen for tour 1, bottom for tour 2, etc., to
  give a sense of progression without being distracting)

### Distribution

- **YouTube** : main platform, video upload (long-form 1h content is
  monetizable)
- **Spotify / Apple Podcasts** : audio only (use final.mp3)
- **Twitter/X clips** : 60s clips of the sharpest exchanges
  - Targets: each debater's strongest 2-min monologue, the
    verdict moment, the rare convergence moments

## Metadata

- **Format**: 3-voice debate (2 debaters + 1 moderator)
- **Language**: English
- **Duration**: ~1h (target)
- **FPS**: 25
- **Audio**: 24 kHz / 16-bit
- **Video codec**: H.264
- **Audio codec**: AAC
- **Audio bitrate**: 192 kbps
- **File**: `video.mp4` (~50-60 MB expected for 1h of static-image 720p)
