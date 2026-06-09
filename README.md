# 🧠 MindClash

> **AI-powered podcast & debate studio** — Turn real conferences, interviews and lectures into deep synthesis podcasts and structured debates between the world's brightest minds.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Local First](https://img.shields.io/badge/local--first-✓-green.svg)]()
[![YouTube Channel](https://img.shields.io/badge/YouTube-MindClash-red.svg)]()

---

## 🎯 What is MindClash?

MindClash is an **AI content production pipeline** that:

1. **Ingests** YouTube videos, playlists, interviews and lectures from any thinker, expert or intellectual worldwide
2. **Analyzes** them in depth using local LLMs (via llama.cpp / Ollama) to extract positions, arguments, key ideas and citations
3. **Produces** two types of high-quality audio content:
   - 🎙️ **Synthesis Podcasts** — deep dives into a topic aggregating multiple sources from several voices
   - ⚔️ **Debate Episodes** — structured AI-moderated clashes between two real thinkers with opposing views
4. **Publishes** to YouTube, Spotify, Apple Podcasts and RSS feeds

MindClash is the fusion of two battle-tested projects:
- **[YT-Insight](https://github.com/nikodindon/YT-Insight)** — deep YouTube analysis pipeline (transcription + LLM analysis → Markdown)
- **[Arena](https://github.com/nikodindon/Arena)** — structured AI debate engine (4-round moderated debate, JSON output)

**Built local-first.** No OpenAI API costs. Runs on consumer hardware (tested on NVIDIA GTX 1650 Super 4GB).

---

## ✨ Core Philosophy

- **Grounded in reality** — every argument is sourced from actual speeches, interviews and lectures, never hallucinated
- **Transnational** — pair experts who would never meet in real life (Jancovici 🇫🇷 vs Amory Lovins 🇺🇸, LeCun vs Hinton...)
- **Local-first** — your knowledge base, your compute, your content
- **Editorial variety** — alternate between synthesis episodes and debate episodes depending on the topic
- **Language-agnostic** — analyze sources in any language, produce output in English (or any target language)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MindClash Pipeline                          │
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │  INGEST      │    │  ANALYZE     │    │  PRODUCE             │  │
│  │              │    │              │    │                      │  │
│  │ • yt-dlp     │───▶│ • Whisper    │───▶│ • Script Generator   │  │
│  │ • Playlists  │    │ • LLM local  │    │ • TTS Engine         │  │
│  │ • Single URL │    │ • Chunking   │    │ • Audio Mixer        │  │
│  │ • Batch      │    │ • Prompts    │    │ • Video Generator    │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│          │                  │                       │               │
│          ▼                  ▼                       ▼               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    KNOWLEDGE BASE                            │   │
│  │  knowledge_base/                                             │   │
│  │  ├── science/                                                │   │
│  │  │   ├── jancovici/          (energy, climate)               │   │
│  │  │   ├── lecun/              (AI, deep learning)             │   │
│  │  │   └── hinton/             (AI safety, neural nets)        │   │
│  │  ├── society/                                                │   │
│  │  │   ├── harari/             (history, future)               │   │
│  │  │   └── zuboff/             (surveillance capitalism)       │   │
│  │  ├── economics/                                              │   │
│  │  │   ├── piketty/            (inequality)                    │   │
│  │  │   └── acemoglu/           (institutions, AI & work)       │   │
│  │  ├── politics/                                               │   │
│  │  └── sport/                                                  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│          │                                                           │
│          ▼                                                           │
│  ┌──────────────────────┐    ┌──────────────────────────────────┐   │
│  │  SYNTHESIS MODE      │    │  DEBATE MODE                     │   │
│  │                      │    │                                  │   │
│  │  N sources →         │    │  Person A sources +              │   │
│  │  1 deep podcast      │    │  Person B sources →              │   │
│  │  (1 or 2 hosts)      │    │  Arena engine →                  │   │
│  │                      │    │  structured debate podcast       │   │
│  └──────────────────────┘    └──────────────────────────────────┘   │
│                    │                        │                        │
│                    └────────────┬───────────┘                        │
│                                 ▼                                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     PUBLISH                                  │   │
│  │  • MP3 audio  • YouTube video  • RSS feed  • Show notes MD   │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
mindclash/
│
├── mindclash/                    # Core Python package
│   ├── __init__.py
│   ├── cli.py                    # Typer CLI — main entry point
│   │
│   ├── ingest/                   # Phase 1: Data collection
│   │   ├── __init__.py
│   │   ├── base.py               # BaseIngestor ABC
│   │   ├── downloader.py         # yt-dlp wrapper (single + playlist)
│   │   ├── playlist.py           # PlaylistProcessor (parallel, resume)
│   │   └── batch.py              # BatchProcessor (multiple playlists/persons)
│   │
│   ├── transcribe/               # Phase 2: Audio → Text
│   │   ├── __init__.py
│   │   ├── base.py               # BaseTranscriber ABC
│   │   ├── faster_whisper.py     # faster-whisper (local, int8 CUDA)
│   │   └── cache.py              # Transcription cache manager
│   │
│   ├── analyze/                  # Phase 3: Text → Knowledge
│   │   ├── __init__.py
│   │   ├── base.py               # BaseAnalyzer ABC
│   │   ├── llamacpp_local.py     # llama.cpp OpenAI-compat API
│   │   ├── ollama.py             # Ollama backend (optional)
│   │   ├── chunker.py            # Smart text chunking + merge
│   │   ├── prompts/
│   │   │   ├── analysis_standard.py
│   │   │   ├── analysis_extreme.py   # depth=extreme
│   │   │   ├── position_paper.py     # Extract person's core positions
│   │   │   ├── synthesis.py          # Cross-video synthesis
│   │   │   └── persona.py            # Build debate persona from MDs
│   │   └── position_extractor.py # Extract argumentative positions
│   │
│   ├── knowledge/                # Phase 4: Knowledge Base management
│   │   ├── __init__.py
│   │   ├── kb_manager.py         # CRUD on knowledge_base/
│   │   ├── indexer.py            # Index all MDs for fast retrieval
│   │   ├── person.py             # Person profile: bio + positions + sources
│   │   └── topic.py              # Topic: cross-person analysis
│   │
│   ├── debate/                   # Phase 5: Debate engine (Arena core)
│   │   ├── __init__.py
│   │   ├── arena.py              # Main debate orchestrator
│   │   ├── debater.py            # Debater agent (persona + sources)
│   │   ├── moderator.py          # AI moderator (scoring, fact-check, flow)
│   │   ├── rounds.py             # Round manager (opening, rebuttals, closing)
│   │   ├── scorer.py             # Argument quality scorer
│   │   └── prep.py               # DebatePrep: topic selection + matchmaking
│   │
│   ├── podcast/                  # Phase 6: Podcast production
│   │   ├── __init__.py
│   │   ├── script_writer.py      # LLM → conversational podcast script
│   │   ├── script_formats/
│   │   │   ├── synthesis.py      # 1 or 2 hosts, deep dive format
│   │   │   ├── debate_cast.py    # Debate → podcast script adapter
│   │   │   └── interview.py      # Reconstructed interview format
│   │   ├── tts/
│   │   │   ├── base.py           # BaseTTS ABC
│   │   │   ├── piper.py          # Piper TTS (fast, local, CPU)
│   │   │   ├── kokoro.py         # Kokoro TTS (high quality)
│   │   │   ├── orpheus.py        # Orpheus TTS (most natural, 2025)
│   │   │   └── voice_profiles.py # Voice assignments per character/show
│   │   ├── mixer.py              # Audio assembly (ffmpeg): segments + music + SFX
│   │   ├── chapters.py           # Chapter markers generator
│   │   └── show_notes.py         # Show notes MD + timestamps generator
│   │
│   ├── publish/                  # Phase 7: Distribution
│   │   ├── __init__.py
│   │   ├── video_builder.py      # Static image + audiogram → MP4 (ffmpeg)
│   │   ├── thumbnail.py          # Thumbnail generator (PIL + templates)
│   │   ├── rss_feed.py           # RSS feed builder (Podcast 2.0 compliant)
│   │   └── metadata.py           # YouTube/Spotify metadata formatter
│   │
│   └── utils/
│       ├── config.py             # YAML + .env config loader
│       ├── logger.py             # Rich logging
│       ├── estimator.py          # Time + cost estimator before run
│       ├── text_utils.py         # Cleaning, truncation, token counting
│       └── ffmpeg_utils.py       # ffmpeg helpers
│
├── knowledge_base/               # 📚 Your growing content library
│   ├── science/
│   │   ├── jancovici/
│   │   │   ├── _profile.md       # Bio + core positions + summary
│   │   │   ├── cours-mines-2024/ # Playlist folder
│   │   │   │   ├── index.md
│   │   │   │   ├── 01-titre.md
│   │   │   │   └── ...
│   │   │   └── interviews/
│   │   ├── lovins/
│   │   └── hinton/
│   ├── society/
│   ├── economics/
│   ├── politics/
│   └── sport/
│
├── episodes/                     # 🎙️ Produced episodes
│   ├── EP001_jancovici-vs-lovins_nuclear-energy/
│   │   ├── debate_raw.json       # Arena output
│   │   ├── script.json           # Podcast script (segmented)
│   │   ├── audio_segments/       # TTS segments
│   │   ├── final_audio.mp3
│   │   ├── final_video.mp4
│   │   ├── thumbnail.png
│   │   └── show_notes.md
│   └── EP002_lecun-vs-hinton_ai-safety/
│
├── assets/
│   ├── music/                    # Royalty-free background tracks
│   ├── sfx/                      # Intro jingle, transitions, etc.
│   ├── thumbnails/               # Thumbnail templates
│   └── voices/                   # TTS voice model files
│
├── config/
│   ├── mindclash.yaml            # Main config
│   ├── voices.yaml               # Voice profiles per character
│   ├── channels.yaml             # YouTube channel config
│   └── prompts/                  # Custom prompt overrides
│
├── tests/
│   ├── test_ingest.py
│   ├── test_analyze.py
│   ├── test_debate.py
│   ├── test_podcast.py
│   └── fixtures/
│
├── docs/
│   ├── PIPELINE.md
│   ├── KNOWLEDGE_BASE.md
│   ├── DEBATE_ENGINE.md
│   ├── TTS_GUIDE.md
│   ├── PUBLISHING.md
│   └── EDITORIAL_GUIDE.md
│
├── pyproject.toml
├── .env.example
└── README.md
```

---

## 🖥️ CLI Reference

### Ingest — Build your Knowledge Base

```bash
# Ingest a single video into a person's folder
mindclash ingest video "https://youtube.com/watch?v=..." --person jancovici --category science --depth extreme

# Ingest a full playlist
mindclash ingest playlist "https://youtube.com/playlist?list=..." --person jancovici --name "cours-mines-2024" --depth extreme --parallel 2

# Ingest multiple playlists for a person (batch)
mindclash ingest batch jancovici --file playlists_jancovici.txt --depth extreme

# Show knowledge base stats
mindclash kb stats
mindclash kb show jancovici
mindclash kb list --category science
```

### Synthesize — Deep Synthesis Podcast

```bash
# Generate synthesis from all sources on a topic
mindclash synthesize --topic "nuclear energy transition" --sources jancovici --depth extreme --length 25min

# Multi-source synthesis (several thinkers on same topic)
mindclash synthesize \
  --topic "future of artificial intelligence" \
  --sources lecun,hinton,bengio \
  --format two-hosts \
  --length 35min \
  --language en

# Full pipeline: synthesize → TTS → mix → video
mindclash synthesize ... --produce --publish-ready
```

### Debate — Structured AI Debate

```bash
# Prepare a debate (topic selection + persona extraction)
mindclash debate prep \
  --person-a jancovici \
  --person-b lovins \
  --topic "Is nuclear energy the only viable path to carbon neutrality?" \
  --rounds 5

# Run the debate
mindclash debate run --config debate_prep.json

# Full pipeline: debate → podcast script → TTS → mix → video
mindclash debate full \
  --person-a jancovici \
  --person-b lovins \
  --topic "nuclear energy" \
  --rounds 5 \
  --length 30min \
  --produce

# Inspect debate output
mindclash debate show episodes/EP001_jancovici-vs-lovins/debate_raw.json
```

### Produce — Audio & Video Production

```bash
# Generate podcast script from existing debate JSON
mindclash produce script --input debate_raw.json --format debate-cast --length 25min

# TTS rendering
mindclash produce tts --input script.json --engine orpheus --voices voices.yaml

# Mix audio (segments + music + SFX)
mindclash produce mix --input audio_segments/ --music ambient_tech --output final_audio.mp3

# Generate video (audiogram + thumbnail)
mindclash produce video --audio final_audio.mp3 --thumbnail thumbnail.png --chapters chapters.json

# Full produce from script to video
mindclash produce full --episode EP001_jancovici-vs-lovins
```

### Estimate — Before you run

```bash
# Estimate time and resources before a long run
mindclash estimate playlist "https://youtube.com/playlist?list=..." --depth extreme
# → 8 videos | ~4h transcription | ~2h analysis | ~45min TTS | Estimated total: 7h
```

---

## 🧩 Module Details

### 1. Ingest Module

Handles all data collection and knowledge base organization.

**PlaylistProcessor** — key features:
- Resume interrupted runs (tracks completed videos in `playlist_state.json`)
- Configurable parallelism (`--parallel N`, default 2 to respect VRAM)
- Auto-generates `index.md` with table of contents, total duration, topic summary
- Detects duplicates (same video ID already in KB)
- Rate limiting and retry logic for yt-dlp

**Knowledge Base structure per person:**
```
knowledge_base/science/jancovici/
├── _profile.md          ← Auto-generated: bio, core positions, key themes, notable quotes
├── _index.md            ← All sources list with dates and topics
├── cours-mines-2024/
│   ├── index.md         ← Playlist synthesis + TOC
│   ├── 01_energie_et_croissance.md
│   └── ...
└── interviews/
    ├── france_inter_2023.md
    └── ...
```

### 2. Analyze Module

Deep analysis using local LLMs with intelligent chunking.

**Depth levels** (inherited from YT-Insight):
- `standard` — summary + key points (~1500 tokens output)
- `deep` — + detailed analysis + notable quotes
- `extreme` — + full structured argumentation + implications + full transcript

**Position Extractor** (new in MindClash):
Runs after standard analysis to extract a machine-readable position paper:

```json
{
  "person": "jancovici",
  "topic": "nuclear energy",
  "core_thesis": "Nuclear is the only low-carbon energy dense enough to sustain industrial civilization",
  "main_arguments": [
    {"id": "arg_01", "claim": "...", "evidence": "...", "source": "cours-mines-2024/03.md", "timestamp": "14:32"},
    ...
  ],
  "acknowledged_weaknesses": [...],
  "red_lines": ["opposes degrowth framing", "skeptical of 100% renewable scenarios"],
  "rhetorical_style": "engineer-pragmatist, data-heavy, provocative",
  "key_quotes": [...]
}
```

This position paper is the core input for the Debate Engine.

### 3. Knowledge Module

**KBManager** — unified interface to the knowledge base:
- `kb.get_person_profile(name)` → full person object
- `kb.get_sources_on_topic(topic, person=None)` → filtered MDs
- `kb.search(query, top_k=10)` → semantic search (optional, via local embeddings)
- `kb.export_context(persons, topic, max_tokens)` → builds LLM-ready context from KB

**PersonProfile** object:
```python
@dataclass
class PersonProfile:
    name: str
    category: str            # science / society / economics / ...
    bio: str
    core_positions: dict     # topic → PositionPaper
    source_files: list[Path] # all .md files for this person
    total_duration_hours: float
    languages: list[str]
    last_updated: datetime
```

### 4. Debate Engine (Arena core, enhanced)

Built on Arena's proven 4-round structure, significantly enhanced for MindClash.

**Debate flow:**
```
DebatePrep
  ├── Topic refinement (LLM-assisted, from KB analysis)
  ├── Persona A extraction (from position papers + KB)
  ├── Persona B extraction
  └── Moderator briefing (rules + scoring criteria)

Debate (N rounds)
  ├── Round 1: Opening statements (each debater states core thesis)
  ├── Round 2-N-1: Rebuttals + counter-arguments
  │     └── Moderator intervenes if: off-topic / strawman / factual drift
  └── Round N: Closing statements

Post-debate
  ├── Moderator final summary + scoring
  ├── Fact-check report (flagged claims vs KB sources)
  └── debate_raw.json export
```

**DebaterAgent** system prompt structure:
```
You are [PERSON_NAME], [SHORT_BIO].

Your core positions on [TOPIC]:
[POSITION_PAPER_CONTENT]

Supporting evidence from your actual speeches and interviews:
[RELEVANT_KB_EXCERPTS — max 8000 tokens]

Rules:
- Argue only from positions and data consistent with your documented views
- You may be pushed into positions you haven't stated publicly: extrapolate carefully
- Your rhetorical style: [STYLE_DESCRIPTION]
- Language: English
- Round type: [opening/rebuttal/closing]
```

**Moderator** enhancements vs Arena v1:
- Scores each argument on: clarity, evidence quality, relevance, novelty
- Detects and flags strawman attacks
- Cross-references claims against KB (basic fact-checking)
- Manages speaking time equity
- Produces a `verdict.md` with winner assessment and key turning points

### 5. Podcast Module

**ScriptWriter** — converts debate JSON or synthesis analysis into natural conversational audio script.

Script JSON format:
```json
{
  "episode_id": "EP001",
  "format": "debate-cast",
  "total_duration_estimate": "28min",
  "segments": [
    {
      "id": "seg_001",
      "speaker": "moderator",
      "voice_profile": "host_neutral",
      "text": "Welcome to MindClash. Today we witness a clash that could never happen in real life...",
      "duration_estimate": "45s",
      "pause_after_ms": 800,
      "music": "fade_out"
    },
    {
      "id": "seg_002",
      "speaker": "jancovici",
      "voice_profile": "expert_french_male",
      "text": "Thank you. The question before us is not ideological — it is purely thermodynamic...",
      "duration_estimate": "90s",
      "emotion": "confident",
      "pause_after_ms": 400
    },
    ...
  ]
}
```

**TTS Engine selection guide** (for GTX 1650 Super 4GB):

| Engine | Quality | Speed | VRAM | Best for |
|--------|---------|-------|------|---------|
| Piper TTS | Good | Very fast (CPU) | 0 | Quick iteration, French |
| Kokoro TTS | Very good | Fast (CPU/GPU) | ~1GB | Production, multilingual |
| **Orpheus TTS** | **Excellent** | **Medium** | **~2GB** | **Final production** |
| XTTS-v2 | Excellent + clone | Slow | ~3GB | Voice cloning experiments |

**Voice profiles** (`config/voices.yaml`):
```yaml
voices:
  host_neutral:
    engine: orpheus
    model: orpheus-en-neutral
    speed: 1.0
    pitch: 0
    style: "calm, clear, authoritative"

  expert_french_male:
    engine: orpheus
    model: orpheus-en-french-accent
    speed: 0.95
    style: "precise, data-driven, slightly provocative"

  expert_american_male:
    engine: orpheus
    model: orpheus-en-us-male
    speed: 1.0
    style: "passionate, optimistic, visionary"
```

**AudioMixer** pipeline (ffmpeg-based):
```
[TTS segments] → normalize loudness → add breath pauses
      ↓
[Background music] → ducking when speech active
      ↓
[Intro jingle] + [segments] + [transition SFX] + [outro]
      ↓
[Master mix] → MP3 320kbps + WAV 24bit/48kHz
```

### 6. Publish Module

**VideoBuilder** — generates YouTube-ready MP4:
- Static debate image with both "fighters" (PIL-generated)
- Animated waveform audiogram overlay
- Auto-generated chapter markers
- Burned-in subtitles (optional, via whisper re-transcription of TTS)

**RSSFeed** — Podcast 2.0 compliant:
- Per-channel RSS (one channel = one category or one debate series)
- Chapter markers (Podcasting 2.0 `<podcast:chapters>`)
- Person tags, location tags
- Auto-submit to Spotify for Podcasters + Apple Podcasts Connect

---

## 🗃️ Knowledge Base — Editorial Strategy

### Categories & Suggested Thinkers

**🔬 Science & Technology**
- `jancovici` — energy, climate, degrowth skeptic (FR)
- `lovins` — efficiency, renewables, anti-nuclear (US)
- `lecun` — AI, autonomous intelligence (FR/US)
- `hinton` — AI safety, existential risk (UK/CA)
- `kaku` — futurism, physics (US)

**💹 Economics**
- `piketty` — inequality, capital (FR)
- `acemoglu` — institutions, AI & labor (US/TR)
- `taleb` — risk, antifragility (LB/US)
- `sachs` — development, sustainability (US)

**🌍 Society & Philosophy**
- `harari` — history, future, transhumanism (IL)
- `zuboff` — surveillance capitalism (US)
- `chomsky` — linguistics, politics, power (US)
- `slavoj_zizek` — ideology, culture (SI)

**🏛️ Politics**
- Topic-based rather than personality-based (avoid direct political impersonation)

**⚽ Sport**
- `klopp` — management philosophy (DE)
- `mourinho` — winning culture (PT)
- Performance science, sports psychology figures

### Debate Matchup Ideas

| Episode | Person A | Person B | Topic |
|---------|----------|----------|-------|
| EP001 | Jancovici 🇫🇷 | Amory Lovins 🇺🇸 | Nuclear vs 100% Renewables |
| EP002 | LeCun 🇫🇷 | Hinton 🇨🇦 | AI Autonomy vs AI Safety |
| EP003 | Piketty 🇫🇷 | Acemoglu 🇺🇸 | AI & Inequality: Tax or Regulate? |
| EP004 | Harari 🇮🇱 | Zuboff 🇺🇸 | Surveillance: Inevitable or Resistible? |
| EP005 | Jancovici 🇫🇷 | Sachs 🇺🇸 | Degrowth vs Green Growth |
| EP006 | LeCun 🇫🇷 | Chomsky 🇺🇸 | Can LLMs truly understand language? |

---

## ⚙️ Configuration

### `config/mindclash.yaml`

```yaml
# LLM Backend
llm:
  backend: llamacpp-local          # llamacpp-local | ollama | openai-compat
  base_url: "http://localhost:8080/v1"
  model: "Qwen3.6-35B-A3B-UD-IQ4_XS.gguf"
  max_tokens: 4096
  temperature: 0.7
  context_window: 32768

# Transcription
transcription:
  backend: faster-whisper
  model: large-v3
  device: cuda
  compute_type: int8
  language: auto                   # auto-detect

# Analysis defaults
analysis:
  default_depth: extreme
  language_output: en              # Output language (en for the channel)
  
# Debate Engine
debate:
  default_rounds: 5
  moderator_model: same            # Use same LLM backend
  max_context_tokens: 24000        # KB context injected per debater
  scoring: true
  fact_check: basic                # basic | none | strict

# TTS
tts:
  default_engine: orpheus
  sample_rate: 48000
  output_format: wav

# Audio Production
audio:
  background_music_volume: 0.08   # 8% volume under speech
  intro_duration_sec: 8
  outro_duration_sec: 12
  normalize_lufs: -16             # Podcast standard

# Knowledge Base
knowledge_base:
  root: ./knowledge_base
  cache_dir: ./cache
  max_context_per_person: 50000   # tokens

# Output
output:
  episodes_dir: ./episodes
  assets_dir: ./assets
```

---

## 🚀 Roadmap

### v0.1 — Foundation (current focus)
- [x] YT-Insight core pipeline (single video)
- [ ] Playlist support with parallel processing
- [ ] Auto-generated `index.md` per playlist
- [ ] KB folder structure + person profiles
- [ ] Cross-playlist synthesis (`mindclash synthesize`)

### v0.2 — Debate Engine
- [ ] Port Arena core → `mindclash/debate/`
- [ ] DebatePrep module (persona extraction from KB)
- [ ] Enhanced moderator (scoring + fact-check)
- [ ] `debate_raw.json` structured output
- [ ] CLI: `mindclash debate full`

### v0.3 — Audio Production
- [ ] ScriptWriter (debate-cast + synthesis formats)
- [ ] Orpheus TTS integration
- [ ] AudioMixer (ffmpeg pipeline)
- [ ] Basic video generation (static image + waveform)
- [ ] First episode produced end-to-end: **EP001 Jancovici vs Lovins**

### v0.4 — Publishing
- [ ] RSS feed generator (Podcast 2.0)
- [ ] YouTube metadata auto-formatter
- [ ] Thumbnail generator
- [ ] Show notes with timestamps

### v0.5 — Scale & Quality
- [ ] Semantic search on KB (local embeddings)
- [ ] Voice cloning experiments (XTTS-v2)
- [ ] Multi-language output support
- [ ] Episode quality scoring (pre-publish check)
- [ ] Web dashboard for KB browsing

### v1.0 — Channel Launch 🎉
- [ ] 5+ episodes produced and published
- [ ] Automated weekly production pipeline
- [ ] Public GitHub release

---

## 🛠️ Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/mindclash.git
cd mindclash

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install
pip install -e ".[dev]"

# Copy config
cp .env.example .env
cp config/mindclash.yaml.example config/mindclash.yaml

# Check setup
mindclash check
# → LLM backend: ✓ (llama.cpp running at localhost:8080)
# → Whisper: ✓ (faster-whisper large-v3, CUDA int8)
# → TTS: ✓ (Orpheus, 2 voices loaded)
# → ffmpeg: ✓
# → Knowledge base: 0 persons, 0 sources
```

### Requirements

- Python 3.11+
- CUDA-capable GPU (tested: GTX 1650 Super 4GB)
- ffmpeg
- llama.cpp server running (or Ollama)
- faster-whisper
- Orpheus TTS (or Piper as fallback)

---

## 🎙️ Example: Full Episode Production

```bash
# Step 1: Build Jancovici's knowledge base
mindclash ingest playlist \
  "https://www.youtube.com/playlist?list=PLMDQXkItOZ4LPwWJkVQf_PWnYHfC5xGFO" \
  --person jancovici --category science --name cours-mines-2024 --depth extreme

# Step 2: Build Lovins' knowledge base
mindclash ingest playlist \
  "https://www.youtube.com/playlist?list=..." \
  --person lovins --category science --name rmi-lectures --depth extreme

# Step 3: Prepare the debate
mindclash debate prep \
  --person-a jancovici \
  --person-b lovins \
  --topic "Is nuclear the only viable path to carbon neutrality by 2050?" \
  --rounds 5 \
  --output prep_EP001.json

# Step 4: Run debate + produce podcast + generate video
mindclash debate full --config prep_EP001.json \
  --episode-id EP001 \
  --length 30min \
  --produce \
  --video

# Output:
# episodes/EP001_jancovici-vs-lovins/
# ├── debate_raw.json
# ├── script.json
# ├── final_audio.mp3       ← ready to upload
# ├── final_video.mp4       ← ready for YouTube
# ├── thumbnail.png
# └── show_notes.md         ← copy-paste YouTube description
```

---

## 🔗 Related Projects

- **[YT-Insight](https://github.com/nikodindon/YT-Insight)** — The analysis engine powering MindClash's ingest phase
- **[Arena](https://github.com/nikodindon/Arena)** — The debate engine at MindClash's core

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## ⚠️ Disclaimer

MindClash generates AI-synthesized content based on publicly available speeches and interviews. All episodes clearly disclose AI generation. Personas are built from documented public positions only. This project does not claim to represent the actual views of any living person beyond what they have publicly stated.

---

*Built with 🧠 by [nikodindon](https://github.com/nikodindon) — Powered by YT-Insight + Arena*
