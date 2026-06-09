#!/usr/bin/env python3
"""
MindClash — Project Structure Setup Script
Run once after cloning the repo to create all directories and placeholder files.
Usage: python setup_mindclash.py
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent

# ── ANSI colors ────────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
BLUE   = "\033[94m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def mkdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def touch(path: Path, content: str = ""):
    if not path.exists():
        path.write_text(content, encoding="utf-8")

def header(title: str):
    print(f"\n{BOLD}{BLUE}{'─'*55}{RESET}")
    print(f"{BOLD}{BLUE}  {title}{RESET}")
    print(f"{BOLD}{BLUE}{'─'*55}{RESET}")

def created(path: Path):
    rel = path.relative_to(ROOT)
    kind = "📁" if path.is_dir() else "📄"
    print(f"  {GREEN}{kind} {rel}{RESET}")

# ══════════════════════════════════════════════════════════════════════════════
# PLACEHOLDERS
# ══════════════════════════════════════════════════════════════════════════════

INIT_PY = '"""MindClash package."""\n'

GITKEEP = ""  # empty, just to keep the folder in git

def make_init(path: Path):
    touch(path / "__init__.py", INIT_PY)

# ══════════════════════════════════════════════════════════════════════════════
# 1. CORE PYTHON PACKAGE
# ══════════════════════════════════════════════════════════════════════════════

def create_package():
    header("1/7  Core Python package — mindclash/")

    pkg = ROOT / "mindclash"
    mkdir(pkg)
    make_init(pkg)
    touch(pkg / "cli.py", '"""MindClash CLI — Typer entry point."""\n')
    created(pkg)

    # Sub-packages
    subpkgs = {
        "ingest":    ["base.py", "downloader.py", "playlist.py", "batch.py"],
        "transcribe":["base.py", "faster_whisper.py", "cache.py"],
        "analyze":   ["base.py", "llamacpp_local.py", "ollama.py",
                      "chunker.py", "position_extractor.py"],
        "knowledge": ["kb_manager.py", "indexer.py", "person.py", "topic.py"],
        "debate":    ["arena.py", "debater.py", "moderator.py",
                      "rounds.py", "scorer.py", "prep.py"],
        "podcast":   ["script_writer.py", "mixer.py", "chapters.py", "show_notes.py"],
        "publish":   ["video_builder.py", "thumbnail.py", "rss_feed.py", "metadata.py"],
        "utils":     ["config.py", "logger.py", "estimator.py",
                      "text_utils.py", "ffmpeg_utils.py"],
    }

    for sub, files in subpkgs.items():
        d = pkg / sub
        mkdir(d)
        make_init(d)
        for f in files:
            touch(d / f, f'"""MindClash — {sub}/{f}."""\n')
        created(d)

    # analyze/prompts sub-package
    prompts_dir = pkg / "analyze" / "prompts"
    mkdir(prompts_dir)
    make_init(prompts_dir)
    for f in ["analysis_standard.py", "analysis_extreme.py",
              "position_paper.py", "synthesis.py", "persona.py"]:
        touch(prompts_dir / f, f'"""Prompt: {f.replace(".py","")}."""\n')
    created(prompts_dir)

    # podcast/tts sub-package
    tts_dir = pkg / "podcast" / "tts"
    mkdir(tts_dir)
    make_init(tts_dir)
    for f in ["base.py", "piper.py", "kokoro.py", "orpheus.py", "voice_profiles.py"]:
        touch(tts_dir / f, f'"""TTS engine: {f.replace(".py","")}."""\n')
    created(tts_dir)

    # podcast/script_formats sub-package
    fmt_dir = pkg / "podcast" / "script_formats"
    mkdir(fmt_dir)
    make_init(fmt_dir)
    for f in ["synthesis.py", "debate_cast.py", "interview.py"]:
        touch(fmt_dir / f, f'"""Script format: {f.replace(".py","")}."""\n')
    created(fmt_dir)

# ══════════════════════════════════════════════════════════════════════════════
# 2. KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════

PROFILE_TEMPLATE = """\
# {name} — Profile

## Bio
> To be filled. Add a short bio here.

## Core Positions
> Run `mindclash kb profile --person {slug}` to auto-generate from sources.

## Key Themes
- 

## Sources
> Add playlists and interviews via `mindclash ingest`.

## Notable Quotes
> Populated automatically from analysis outputs.
"""

def create_knowledge_base():
    header("2/7  Knowledge Base — knowledge_base/")

    kb = ROOT / "knowledge_base"

    # category → [(slug, display_name)]
    persons = {
        "science": [
            ("jancovici",  "Jean-Marc Jancovici"),
            ("lovins",     "Amory Lovins"),
            ("lecun",      "Yann LeCun"),
            ("hinton",     "Geoffrey Hinton"),
            ("kaku",       "Michio Kaku"),
        ],
        "economics": [
            ("piketty",    "Thomas Piketty"),
            ("acemoglu",   "Daron Acemoglu"),
            ("taleb",      "Nassim Taleb"),
            ("sachs",      "Jeffrey Sachs"),
        ],
        "society": [
            ("harari",     "Yuval Noah Harari"),
            ("zuboff",     "Shoshana Zuboff"),
            ("chomsky",    "Noam Chomsky"),
            ("zizek",      "Slavoj Žižek"),
        ],
        "politics": [],   # topic-based, no persons yet
        "sport": [
            ("klopp",      "Jürgen Klopp"),
            ("mourinho",   "José Mourinho"),
        ],
    }

    for category, people in persons.items():
        cat_dir = kb / category
        mkdir(cat_dir)
        touch(cat_dir / ".gitkeep", GITKEEP)

        for slug, name in people:
            p_dir = cat_dir / slug
            mkdir(p_dir)

            touch(p_dir / "_profile.md",
                  PROFILE_TEMPLATE.format(name=name, slug=slug))
            touch(p_dir / "_index.md",
                  f"# {name} — Source Index\n\n| File | Date | Topic | Duration |\n|------|------|-------|----------|\n")

            # Sub-folders per person
            for sub in ["interviews", "lectures", "articles"]:
                sub_dir = p_dir / sub
                mkdir(sub_dir)
                touch(sub_dir / ".gitkeep", GITKEEP)

        created(cat_dir)

    print(f"  {YELLOW}ℹ  Playlists will be created here by `mindclash ingest playlist`{RESET}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. EPISODES
# ══════════════════════════════════════════════════════════════════════════════

EPISODE_README = """\
# {ep_id} — {title}

## Status
- [ ] Debate generated
- [ ] Script written
- [ ] TTS rendered
- [ ] Audio mixed
- [ ] Video generated
- [ ] Published

## Persons
- **Person A:** {person_a}
- **Person B:** {person_b}

## Topic
> {topic}

## Files
| File | Description |
|------|-------------|
| `debate_raw.json` | Arena debate output |
| `script.json` | Podcast script (segmented) |
| `audio_segments/` | Individual TTS segments |
| `final_audio.mp3` | Master audio |
| `final_video.mp4` | YouTube-ready video |
| `thumbnail.png` | Episode thumbnail |
| `show_notes.md` | YouTube description + timestamps |
"""

def create_episodes():
    header("3/7  Episodes — episodes/")

    ep_dir = ROOT / "episodes"
    mkdir(ep_dir)

    # Seed episodes matching the README matchup table
    seeds = [
        ("EP001", "jancovici-vs-lovins",  "Jancovici", "Lovins",
         "Is nuclear the only viable path to carbon neutrality by 2050?"),
        ("EP002", "lecun-vs-hinton",       "LeCun",    "Hinton",
         "AI Autonomy vs AI Safety: where is the real risk?"),
        ("EP003", "piketty-vs-acemoglu",   "Piketty",  "Acemoglu",
         "AI & Inequality: Tax or Regulate?"),
        ("EP004", "harari-vs-zuboff",      "Harari",   "Zuboff",
         "Surveillance capitalism: inevitable or resistible?"),
        ("EP005", "jancovici-vs-sachs",    "Jancovici","Sachs",
         "Degrowth vs Green Growth: which path for 2050?"),
        ("EP006", "lecun-vs-chomsky",      "LeCun",    "Chomsky",
         "Can LLMs truly understand language?"),
    ]

    for ep_id, slug, pa, pb, topic in seeds:
        d = ep_dir / f"{ep_id}_{slug}"
        mkdir(d)
        touch(d / "README.md",
              EPISODE_README.format(ep_id=ep_id, title=f"{pa} vs {pb}",
                                    person_a=pa, person_b=pb, topic=topic))
        touch(d / "debate_raw.json",   "")
        touch(d / "script.json",       "")
        touch(d / "show_notes.md",     f"# {ep_id} Show Notes\n\n## Timestamps\n\n")
        mkdir(d / "audio_segments")
        touch(d / "audio_segments" / ".gitkeep", GITKEEP)
        created(d)

# ══════════════════════════════════════════════════════════════════════════════
# 4. ASSETS
# ══════════════════════════════════════════════════════════════════════════════

def create_assets():
    header("4/7  Assets — assets/")

    assets = ROOT / "assets"
    for sub in ["music", "sfx", "thumbnails", "voices"]:
        d = assets / sub
        mkdir(d)
        touch(d / ".gitkeep", GITKEEP)
        touch(d / "README.md", f"# {sub.capitalize()}\n\nPlace {sub} files here.\n")
        created(d)

# ══════════════════════════════════════════════════════════════════════════════
# 5. CONFIG
# ══════════════════════════════════════════════════════════════════════════════

MINDCLASH_YAML = """\
# MindClash — Main Configuration
# Copy this file to mindclash.yaml and edit to match your setup.

# ── LLM Backend ───────────────────────────────────────────────────────────────
llm:
  backend: llamacpp-local          # llamacpp-local | ollama | openai-compat
  base_url: "http://localhost:8080/v1"
  model: "Qwen3.6-35B-A3B-UD-IQ4_XS.gguf"
  max_tokens: 4096
  temperature: 0.7
  context_window: 32768

# ── Transcription ─────────────────────────────────────────────────────────────
transcription:
  backend: faster-whisper
  model: large-v3
  device: cuda
  compute_type: int8
  language: auto

# ── Analysis ──────────────────────────────────────────────────────────────────
analysis:
  default_depth: extreme           # standard | deep | extreme
  language_output: en

# ── Debate Engine ─────────────────────────────────────────────────────────────
debate:
  default_rounds: 5
  moderator_model: same
  max_context_tokens: 24000
  scoring: true
  fact_check: basic                # basic | none | strict

# ── TTS ───────────────────────────────────────────────────────────────────────
tts:
  default_engine: orpheus          # orpheus | kokoro | piper
  sample_rate: 48000
  output_format: wav

# ── Audio Production ──────────────────────────────────────────────────────────
audio:
  background_music_volume: 0.08
  intro_duration_sec: 8
  outro_duration_sec: 12
  normalize_lufs: -16

# ── Knowledge Base ────────────────────────────────────────────────────────────
knowledge_base:
  root: ./knowledge_base
  cache_dir: ./cache
  max_context_per_person: 50000

# ── Output ────────────────────────────────────────────────────────────────────
output:
  episodes_dir: ./episodes
  assets_dir: ./assets
"""

VOICES_YAML = """\
# MindClash — Voice Profiles
# Assign TTS voices to recurring characters.

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

  expert_british_male:
    engine: orpheus
    model: orpheus-en-gb-male
    speed: 0.98
    style: "measured, academic, nuanced"

  moderator:
    engine: orpheus
    model: orpheus-en-neutral
    speed: 1.0
    style: "neutral, firm, engaging"

# Person → voice mapping
person_voices:
  jancovici: expert_french_male
  lovins:    expert_american_male
  lecun:     expert_french_male
  hinton:    expert_british_male
  piketty:   expert_french_male
  acemoglu:  expert_american_male
  harari:    expert_british_male
  chomsky:   expert_american_male
"""

CHANNELS_YAML = """\
# MindClash — YouTube Channel Configuration

channel:
  name: "MindClash"
  handle: "@MindClashAI"
  description: >
    AI-synthesized debates and deep dives between the world's most brilliant minds.
    Powered by real speeches, lectures and interviews. Every argument is sourced.
  language: en
  category: Education
  tags:
    - AI debates
    - intellectual debates
    - science podcast
    - philosophy
    - economics
    - MindClash

  playlist_ids:
    debates:   ""        # Fill after creating YouTube playlists
    synthesis: ""

podcast:
  rss_title: "MindClash"
  rss_description: >
    Structured AI debates and synthesis podcasts grounded in real thinkers' ideas.
  author: "MindClash AI"
  email: ""
  website: ""
  language: en
  explicit: false
  category: "Society & Culture"
  subcategory: "Philosophy"
"""

ENV_EXAMPLE = """\
# MindClash — Environment Variables
# Copy to .env and fill in your values.

# LLM
LLAMACPP_BASE_URL=http://localhost:8080/v1
OLLAMA_BASE_URL=http://localhost:11434

# TTS (if using cloud fallback)
ELEVENLABS_API_KEY=

# Publishing (optional)
YOUTUBE_CLIENT_SECRETS_FILE=
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
"""

def create_config():
    header("5/7  Config — config/")

    cfg = ROOT / "config"
    mkdir(cfg)

    touch(cfg / "mindclash.yaml.example", MINDCLASH_YAML)
    touch(cfg / "voices.yaml",            VOICES_YAML)
    touch(cfg / "channels.yaml",          CHANNELS_YAML)

    prompts_cfg = cfg / "prompts"
    mkdir(prompts_cfg)
    touch(prompts_cfg / ".gitkeep", GITKEEP)
    touch(prompts_cfg / "README.md",
          "# Custom Prompt Overrides\n\nPlace `.txt` prompt overrides here.\n"
          "Files here take precedence over defaults in `mindclash/analyze/prompts/`.\n")

    touch(ROOT / ".env.example", ENV_EXAMPLE)
    created(cfg)

# ══════════════════════════════════════════════════════════════════════════════
# 6. TESTS
# ══════════════════════════════════════════════════════════════════════════════

TEST_TEMPLATE = """\
\"\"\"Tests for mindclash.{module}.\"\"\"
import pytest


def test_placeholder():
    \"\"\"Placeholder — replace with real tests.\"\"\"
    assert True
"""

def create_tests():
    header("6/7  Tests — tests/")

    tests = ROOT / "tests"
    mkdir(tests)
    touch(tests / "__init__.py", "")
    touch(tests / "conftest.py",
          '"""Shared pytest fixtures for MindClash tests."""\nimport pytest\n')

    for module in ["ingest", "transcribe", "analyze", "knowledge",
                   "debate", "podcast", "publish"]:
        touch(tests / f"test_{module}.py", TEST_TEMPLATE.format(module=module))

    fixtures = tests / "fixtures"
    mkdir(fixtures)
    touch(fixtures / ".gitkeep", GITKEEP)
    touch(fixtures / "README.md",
          "# Test Fixtures\n\nSmall sample files for unit tests.\n")

    created(tests)

# ══════════════════════════════════════════════════════════════════════════════
# 7. ROOT FILES
# ══════════════════════════════════════════════════════════════════════════════

PYPROJECT = """\
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "mindclash"
version = "0.1.0"
description = "AI-powered podcast & debate studio"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "typer[all]>=0.12",
    "rich>=13",
    "httpx>=0.27",
    "pydantic>=2",
    "python-dotenv>=1.0",
    "pyyaml>=6",
    "yt-dlp>=2024",
    "faster-whisper>=1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "pytest-cov",
    "ruff",
    "mypy",
]

[project.scripts]
mindclash = "mindclash.cli:app"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
"""

GITIGNORE = """\
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
venv/

# MindClash runtime
cache/
outputs/
knowledge_base/**/*.mp3
knowledge_base/**/*.wav
episodes/**/audio_segments/
episodes/**/final_audio.mp3
episodes/**/final_video.mp4
assets/voices/*.bin
assets/voices/*.onnx

# Config secrets
.env
config/mindclash.yaml

# OS
.DS_Store
Thumbs.db
"""

MAKEFILE = """\
.PHONY: install dev test lint check clean

install:
\tpip install -e .

dev:
\tpip install -e ".[dev]"

test:
\tpytest tests/ -v --cov=mindclash

lint:
\truff check mindclash/ tests/

check:
\tmindclash check

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {} +
\tfind . -name "*.pyc" -delete
"""

def create_root_files():
    header("7/7  Root files")

    touch(ROOT / "pyproject.toml", PYPROJECT)
    touch(ROOT / ".gitignore",     GITIGNORE)
    touch(ROOT / "Makefile",       MAKEFILE)
    touch(ROOT / "CHANGELOG.md",   "# Changelog\n\n## [0.1.0] — Unreleased\n\n### Added\n- Initial project structure\n")

    # Cache and outputs dirs (gitignored)
    for d in ["cache", "outputs"]:
        mkdir(ROOT / d)
        touch(ROOT / d / ".gitkeep", GITKEEP)

    # Docs
    docs = ROOT / "docs"
    mkdir(docs)
    for doc in ["PIPELINE.md", "KNOWLEDGE_BASE.md", "DEBATE_ENGINE.md",
                "TTS_GUIDE.md", "PUBLISHING.md", "EDITORIAL_GUIDE.md"]:
        touch(docs / doc,
              f"# {doc.replace('.md','').replace('_',' ')}\n\n> Documentation coming soon.\n")
    created(docs)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"\n{BOLD}{'═'*55}")
    print(f"  🧠  MindClash — Project Setup")
    print(f"  Root: {ROOT}")
    print(f"{'═'*55}{RESET}")

    create_package()
    create_knowledge_base()
    create_episodes()
    create_assets()
    create_config()
    create_tests()
    create_root_files()

    # Count what was created
    total_dirs  = sum(1 for _ in ROOT.rglob("*") if _.is_dir())
    total_files = sum(1 for _ in ROOT.rglob("*") if _.is_file())

    print(f"\n{BOLD}{'═'*55}")
    print(f"  {GREEN}✓  Done!{RESET}{BOLD}")
    print(f"  {total_dirs} directories  |  {total_files} files created")
    print(f"{'═'*55}{RESET}")
    print(f"""
{YELLOW}Next steps:{RESET}
  1. {BOLD}cp config/mindclash.yaml.example config/mindclash.yaml{RESET}
     → Edit with your LLM backend URL and model path

  2. {BOLD}cp .env.example .env{RESET}
     → Fill in your API keys if needed

  3. {BOLD}pip install -e ".[dev]"{RESET}
     → Install the package in editable mode

  4. {BOLD}mindclash check{RESET}
     → Verify LLM, Whisper, TTS and ffmpeg are reachable

  5. {BOLD}mindclash ingest playlist <URL> --person jancovici --category science{RESET}
     → Start building your knowledge base 🚀
""")

if __name__ == "__main__":
    main()
