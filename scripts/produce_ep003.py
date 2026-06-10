"""Generate all audio segments for EP003 (Jancovici vs Lovins debate).

Reads episodes/EP003_jancovici-vs-lovins/script.json, runs Kokoro TTS
on each segment with the right voice:
  - debater_a (Jancovici) = am_adam
  - debater_b (Lovins) = am_michael
  - moderator (Bella) = af_bella

Outputs:
  - 64+ individual wav files in audio_segments/
  - master.wav (~1h)
  - final.wav / final.mp3 via mix_ep003.py + render_video_ep003.py
"""
import json
import wave
import numpy as np
from pathlib import Path
from kokoro_onnx import Kokoro

ROOT = Path('/home/niko/MindClash')
SCRIPT_PATH = ROOT / 'episodes/EP003_jancovici-vs-lovins/script.json'
SEGMENTS_DIR = ROOT / 'episodes/EP003_jancovici-vs-lovins/audio_segments'
MASTER_PATH = ROOT / 'episodes/EP003_jancovici-vs-lovins/master.wav'

SAMPLE_RATE = 24000  # Kokoro native

print('Loading Kokoro...')
kokoro = Kokoro(ROOT / 'models/kokoro/kokoro-v0_19.onnx',
                 ROOT / 'models/kokoro/voices.bin')
print('OK\n')

# Load script
data = json.loads(SCRIPT_PATH.read_text())
segments = data['segments']
print(f'Script has {len(segments)} segments')

# Voice mapping (3 voices, see generate_debate_ep003.py)
# Falls back to voice_map in script.json if defined, else hardcoded defaults
voice_map = data.get('voice_map') or {
    "debater_a": "am_adam",
    "debater_b": "am_michael",
    "moderator": "af_bella",
}
print(f"Voice map: {voice_map}")

# Generate each segment
SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)
all_audio = []  # master concat
total_duration_est = 0

for i, seg in enumerate(segments, 1):
    text = seg['text']
    speaker = seg['speaker']
    voice = voice_map[speaker]
    seg_id = seg['id']
    tour = seg.get('tour', 0)
    tour_name = seg.get('tour_name', '?')
    pause_ms = seg.get('pause_after_ms', 800)

    # Generate
    gen = kokoro.create(text, voice=voice, speed=1.0, lang='en-us')
    result = list(gen)
    if isinstance(result[0], tuple):
        samples = result[0][0]
    else:
        samples = result[0]
    if not isinstance(samples, np.ndarray):
        samples = np.concatenate([np.array(r[0]) if isinstance(r, tuple) else np.array(r) for r in result])

    # Convert to int16
    audio_int16 = (np.clip(samples, -1.0, 1.0) * 32767).astype('int16')
    duration = len(audio_int16) / SAMPLE_RATE
    total_duration_est += duration + pause_ms / 1000

    # Save individual segment (filename encodes tour + segment)
    seg_path = SEGMENTS_DIR / f't{tour:02d}_{tour_name[:8]}_seg_{seg_id:03d}_{speaker}.wav'
    with wave.open(str(seg_path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(audio_int16.tobytes())

    # Add a small extra pause between tours (transition sting placeholder)
    extra_pause = 0
    if i < len(segments) and segments[i].get('tour', 0) != tour:
        extra_pause = 2000  # 2s between tours
        print(f'  [tour change {tour}→{segments[i].get("tour")} at seg {i}/{len(segments)}]')

    print(f'  [{i:3d}/{len(segments)}] t{tour}.{tour_name[:6]:6s} seg_{seg_id:03d} {speaker:12s} {voice:11s} ({seg.get("emotion","?"):14s}) {duration:5.1f}s + {pause_ms}ms')

    # Add to master
    all_audio.append(audio_int16)
    if pause_ms > 0:
        silence_samples = int(SAMPLE_RATE * pause_ms / 1000)
        all_audio.append(np.zeros(silence_samples, dtype='int16'))
    if extra_pause > 0:
        silence_samples = int(SAMPLE_RATE * extra_pause / 1000)
        all_audio.append(np.zeros(silence_samples, dtype='int16'))

# Concatenate master
print(f'\nConcatenating {len(all_audio)} chunks...')
master_audio = np.concatenate(all_audio)
master_duration = len(master_audio) / SAMPLE_RATE
print(f'Master duration: {master_duration:.1f}s = {master_duration/60:.1f} min')
print(f'Estimated from text: {total_duration_est:.1f}s = {total_duration_est/60:.1f} min')

# Write master
with wave.open(str(MASTER_PATH), 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SAMPLE_RATE)
    w.writeframes(master_audio.tobytes())

print(f'\n✓ Master saved: {MASTER_PATH} ({MASTER_PATH.stat().st_size/1024/1024:.1f} MB)')
print(f'✓ {len(segments)} segments saved in {SEGMENTS_DIR}/')
