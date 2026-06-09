# MindClash Roadmap

> Living document. Updated as work progresses. Check the [session-handoff](../docs/session-handoff.md) for full history.

## Status legend
- [x] Done
- [~] In progress
- [ ] Backlog

---

## Phase 1 — Pilot validation (EP001)

- [x] Create `episodes/EP001_jancovici-synthesis/` (FR + EN scripts)
- [x] Source material: 8 Mines lectures 2019 by Jancovici
- [x] Knowledge Base: `_profile.md` for Jancovici
- [x] Script v3 (EN, 19.5 min, 64 segments, 2874 words)
- [x] TTS production: Kokoro `am_adam` + `am_michael`
- [x] Audio mix: `final.wav` + `final.mp3` (192 kbps)
- [x] Video render: `video.mp4` (720p, H.264+AAC)
- [x] Custom background image (PIL-generated)
- [x] Show notes (title, description, chapters, tags)
- [x] Pipeline documentation (`docs/PIPELINE.md`)
- [x] `yt-insight-podcast` skill for future sessions
- [ ] **User review and YouTube upload** (current blocker)
- [ ] French version (re-use FR script v2 + Piper Tom/Siwis)
- [ ] Custom thumbnail (1280x720, with topic text + Jancovici photo)

## Phase 2 — Pilot iteration (after upload)

- [ ] Analyze early YouTube metrics (retention, engagement, sentiment)
- [ ] Identify what worked / didn't in the pilot format
- [ ] Adjust format for EP002 (shorter intros? more citations? music?)

## Phase 3 — Debate format (EP002+)

- [ ] Reuse Arena's debate engine (or port it into MindClash)
- [ ] EP002: Jancovici vs Amory Lovins (energy / nuclear vs renewables)
- [ ] Generate 2 profile MDs (Jancovici done; Lovins TODO)
- [ ] Source 5+ MDs per debater (lectures, interviews, articles)
- [ ] Debate script generator: produce JSON with 4 turns + moderator
- [ ] TTS with 3 voices (host + debater1 + debater2)
- [ ] Distinguish personas via voice characteristics

## Phase 4 — Multi-subject expansion

- [ ] Science: Hinton vs LeCun (AI debate)
- [ ] Economics: Piketty vs Acemoglu (inequality)
- [ ] Society: Harari vs Zuboff (surveillance)
- [ ] Sport: Klopp vs Mourinho (football philosophy)
- [ ] Each needs: 2-3 source MDs per personality, profile, script

## Phase 5 — Production tooling

- [ ] Generalize `produce_ep001.py` → `produce_episode.py` (param on episode dir)
- [ ] Generalize `mix_ep001.py` → `mix_episode.py`
- [ ] Generalize `render_video_ep001.py` → `render_video.py`
- [ ] YouTube Data API v3 auto-upload
- [ ] Auto-thumbnail generator (PIL with topic + photo)
- [ ] Twitter clip auto-extraction (cut 60s from punchlines)

## Phase 6 — Quality + scale

- [ ] Cron-based weekly episode production
- [ ] Analytics dashboard (YouTube + Twitter + Spotify)
- [ ] Multi-language pipeline (EN pilot, FR/ES/DE follow)
- [ ] Community feedback loop (comments → next episode topics)

## Backlog (low priority)

- [ ] Spotify/Apple Podcasts auto-distribution
- [ ] Interactive web player (searchable transcripts)
- [ ] Newsletter integration
- [ ] Sponsorship / monetization
- [ ] 4K video upgrade
- [ ] Subtitles in 5+ languages
- [ ] Clip channel (TikTok / Shorts from main episodes)

## Known issues to address

- **Pilote length**: 19.5 min vs target 22-25. Acceptable for v1; can extend for v2.
- **Background**: currently static PNG. v2 could add slow zoom, particle effects, or thermodynamic diagrams.
- **Music**: no section stings yet. Optional addition for v2.
- **Voice distinction**: 2 male voices (am_adam + am_michael) are distinct but not maximally so. Could add slight pitch shift for the host to make it more obvious.

## Decisions log

- **English first** (not French) — bigger audience, easier to get feedback
- **Kokoro over Piper** for English — better quality
- **Piper kept on disk** for future French episodes
- **2-voice interview format** for synthesis episodes, 3-voice for debates
- **No cron yet** — pilot must be validated first
- **Single-commit history** for the project (clean, no model-tracking mess)
