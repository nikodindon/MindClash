# EP002 — Amory Lovins Synthesis

> **Status**: seed only, awaiting Lovins-solo podcast generation
> **Planned release**: after EP001 (Jancovici solo)
> **Format**: same as EP001 — 2 voices (host + expert), English, 20-25 min
> **Teaser target**: ends with "next episode: Jancovici vs Lovins debate" (EP003)

## Persons

- **Person A** (host): Alex
- **Person B** (expert): Marc

## Topic

> The optimistic alternative to the Jancovici-style thermodynamic
> pessimism. After spending EP001 exploring the limits, EP002 explores
> the response: soft energy paths, negawatts, design integratif,
> Reinventing Fire.

## Files

| File | Description | Status |
|------|-------------|--------|
| `README.md` | This file | ✅ |
| `show_notes.md` | YouTube description + timestamps | ⏳ (template below) |
| `script.json` | Podcast script (segmented) | ⏳ |
| `audio_segments/` | Individual TTS segments | ⏳ |
| `master.wav` | Master audio | ⏳ |
| `final.wav` / `final.mp3` | Mixed with intro/outro | ⏳ |
| `video.mp4` | YouTube-ready video | ⏳ |

## KB sources

- 4 talks ingested via YT-Insight (depth=extreme), June 2026
- See `knowledge_base/science/lovins/_profile.md` for the synthesized
  profile and `knowledge_base/science/lovins/_index.md` for sources
- 190 key points + 17 verbatim quotes available

## Production checklist

- [ ] Draft `show_notes.md` (template in this README, fill in once script is written)
- [ ] Generate `script.json` from Lovins `_profile.md` (mirroring EP001 pipeline)
- [ ] Render TTS via Kokoro (Alex=am_adam, Marc=am_michael — same voices as EP001 for continuity)
- [ ] Mix intro/outro music beds
- [ ] Render video (ffmpeg H.264 + AAC, 720p)
- [ ] Add "next episode: Jancovici vs Lovins" teaser in outro (handoff to EP003)
- [ ] Update `knowledge_base/science/lovins/_profile.md` with self-critique section (Qwen generation in progress)
