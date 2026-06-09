# MindClash Production Pipeline

> Complete pipeline to produce a MindClash podcast episode, from source
> knowledge to YouTube-ready video. Documented from the EP001 pilot.

## Overview

```
Knowledge Base (MD files)
       ↓
Profile + Script (JSON)
       ↓
TTS Audio (WAV per segment)
       ↓
Master Audio (WAV concatenated)
       ↓
Final Audio (WAV with music + MP3 export)
       ↓
Video (MP4 with background + audio)
       ↓
YouTube Upload (manual or scripted)
```

## Stage 1 — Knowledge Base

**Input**: Source material — YouTube videos, articles, books
**Output**: Per-personality `_profile.md` + per-source `.md` files

### Tools
- **YT-Insight** (separate project) — pipeline for downloading, transcribing,
  and analyzing YouTube videos into structured MD files
- Manual curation for non-video sources

### Structure
```
knowledge_base/<category>/<personality>/
├── _profile.md                 ← synthesized bio + theses
├── articles/                   ← MD analysis of articles
├── interviews/                 ← MD analysis of interviews
└── lectures/                   ← MD analysis of lectures
```

**Example**: `knowledge_base/science/jancovici/lectures/cours-mines-2019/`
contains 8 MD files (one per lecture) + the `_profile.md` summary.

### Skip rule
Don't import all source material blindly. For each candidate source:
- Does it advance the topic the episode is about?
- Is the speaker's perspective unique / different from others in the KB?
- Is the source substantial enough (15+ min for video, 2000+ words for text)?

## Stage 2 — Script

**Input**: `_profile.md` + relevant source MDs
**Output**: `episodes/EP###_<slug>/script.json`

### Format
```json
{
  "episode": "EP001",
  "title": "The Thermodynamics of Civilization: ...",
  "duration_target_seconds": 1450,
  "language": "en",
  "format": "interview",
  "speakers": {
    "host": {"name": "Alex", "voice_id": "am_adam", "style": "..."},
    "expert": {"name": "Marc", "voice_id": "am_michael", "style": "..."}
  },
  "segments": [
    {
      "id": 1,
      "section": "intro",
      "speaker": "host",
      "text": "...",
      "emotion": "friendly",
      "pause_after_ms": 700
    }
  ]
}
```

### Writing rules
- **Sections**: 6 recommended (intro / context / topic blocks / analysis / outro)
- **Segment length**: 1-3 sentences, 10-80 words (ideal for natural speech breaks)
- **Pauses**: 400-1500ms between segments, longer at section transitions
- **Citations**: include 3-4 verbatim quotes from the source (with timestamp refs)
- **Tone**: conversational, not academic. Read each segment out loud to test.
- **Language**: write in the target language natively, not as a translation

### Length target
- 22-25 min spoken (English: ~150 words/min; French: ~130 wpm)
- 64-80 segments typically
- 3000-3500 words

### Time to write
~2-3 hours for a focused synthesis. More for a debate (4-6 hours).

## Stage 3 — TTS Audio

**Input**: `script.json`
**Output**: `episodes/EP###_<slug>/audio_segments/seg_NNN_<speaker>.wav`

### Tool: Kokoro
- Model: v0.19 ONNX, 24000 Hz, 16-bit
- 11 voices: 4 US/UK male (`am_adam`, `am_michael`, `bm_george`, `bm_lewis`),
  4 US/UK female (`af_bella`, `af_nicole`, `af_sarah`, `af_sky`, `bf_emma`, `bf_isabella`),
  plus `af` (voice mix)
- Install: `pip install kokoro-onnx`
- Download: `kokoro-v0_19.onnx` (310 MB) + `voices.bin` (5.5 MB) from
  `hexgrad/kokoro-onnx` on HuggingFace

### Script: `scripts/produce_ep001.py` (or generalize to `produce_episode.py`)

```python
from kokoro_onnx import Kokoro
kokoro = Kokoro('models/kokoro/kokoro-v0_19.onnx', 'models/kokoro/voices.bin')

voice_map = {'host': 'am_adam', 'expert': 'am_michael'}
chunks = list(kokoro.create(text, voice=voice_map[speaker], speed=1.0, lang='en-us'))
audio_int16 = (np.clip(chunks[0][0], -1.0, 1.0) * 32767).astype('int16')
```

### Time to produce
- 20-30 min for 64 segments on CPU
- ~25 sec per long segment, ~5 sec per short segment
- Watch for the first run: 60-90s model load

### Gotchas
- Kokoro voices don't have French by default — use Piper for FR
- Long segments (40+ sec) are slow; consider splitting
- No GPU needed for Kokoro (CPU is fast enough)
- Save individual segments before concatenating (lets you re-do sections)

## Stage 4 — Master Audio

**Input**: Per-segment WAVs
**Output**: `master.wav` (concatenated, with pauses)

### Process
1. Load each segment
2. Append silence matching `pause_after_ms`
3. Concatenate with `np.concatenate`
4. Write WAV (16-bit, 24000 Hz, mono)

### Time
< 5 seconds for 64 segments.

## Stage 5 — Final Audio + Music

**Input**: `master.wav`
**Output**: `final.wav` (with intro/outro music) + `final.mp3` (192 kbps)

### Process
1. Generate intro music (10s ambient) + outro music (15s ambient)
2. Apply fade-in to intro, fade-out to outro
3. Concatenate: `intro + master + outro`
4. Export to MP3 via ffmpeg + libmp3lame

### Music sources
- **Free libraries**: YouTube Audio Library, Pixabay Music, Uppbeat
- **Format**: WAV or MP3, 24000 Hz (will be resampled if needed)
- **Style**: ambient / minimal / serious (no vocals, no drums for synthesis episodes)
- **Length**: 10-15s for intro, 10-20s for outro
- **Stings**: 2-3s between major sections (optional)

### Script: `scripts/mix_ep001.py`

### Time
< 30 seconds (ffmpeg handles the conversion).

## Stage 6 — Video

**Input**: `final.wav` + background image
**Output**: `video.mp4` (720p, H.264 + AAC)

### Background
- 1280x720 PNG/JPG
- Style: dark, clean, topic-text overlay
- Use `scripts/generate_background.py` to create a default

### Process
```bash
ffmpeg -y -loop 1 -i background.png -i final.wav \
  -c:v libx264 -tune stillimage \
  -c:a aac -b:a 192k \
  -pix_fmt yuv420p -shortest \
  -vf scale=1280:720 \
  video.mp4
```

### Time
3-5 minutes for 20 min video (CPU only).

### Output
~16-22 MB for 20 min at 720p H.264.

## Stage 7 — YouTube Upload

**Input**: `video.mp4` + `show_notes.md` (title, description, tags, chapters)
**Output**: Published video on YouTube

### Manual upload (for the pilot)
1. Go to YouTube Studio
2. Upload `video.mp4`
3. Copy title from `show_notes.md`
4. Copy description (first 200 chars visible above the fold)
5. Add chapters as timestamps in the description
6. Add tags
7. Set thumbnail (custom design — see below)
8. Publish (public, unlisted first for review)

### Custom thumbnail
- 1280x720 image
- Bold readable text (max 5-7 words)
- High contrast (works on mobile)
- See: `assets/thumbnails/thumb_<episode>.jpg`

### Time
15-30 minutes for the first upload (incl. thumbnail design).

## Total time budget for a new episode

| Stage | Time |
|-------|------|
| Knowledge Base | 4-8h (for a debate: 16-24h) |
| Script | 2-3h (synthesis) / 4-6h (debate) |
| TTS Production | 25-35 min (auto) |
| Mix + Video | 5-10 min (auto) |
| YouTube Upload | 30-60 min (incl. thumbnail) |
| **Total** | **~8-12h for synthesis** / **~20-30h for debate** |

## Optimization opportunities (future)

- **Parallel TTS**: use 2-3 Kokoro instances to halve production time
- **Auto-thumbnail**: generate thumbnails from background + a few text overlays
- **Direct YouTube upload**: YouTube Data API v3 (skip manual Studio)
- **Auto Twitter clips**: detect punchlines, cut 60s clips, post with hashtags
- **Skill**: `yt-insight-podcast` automates stages 3-6 (script → MP4)

## Tools used in the EP001 pilot

- `scripts/generate_background.py` — PIL-based background generator
- `scripts/produce_ep001.py` — Kokoro TTS production
- `scripts/mix_ep001.py` — ffmpeg audio mix
- `scripts/render_video_ep001.py` — ffmpeg video render
- `pyproject.toml` — pins all dependencies
