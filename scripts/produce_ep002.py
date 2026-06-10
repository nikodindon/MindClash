"""Generate all audio segments for EP002 (Lovins-solo).

Reads episodes/EP002_lovins-synthesis/script.json, runs Kokoro TTS
on each segment with the right voice (Alex = am_adam, Marc = am_michael),
adds the requested pause_after_ms, and saves individual wav files in
episodes/EP002_lovins-synthesis/audio_segments/.

Final master: episodes/EP002_lovins-synthesis/master.wav

Mirrors produce_ep001.py exactly, just with paths pointed at EP002.
The voices are the same as EP001 (am_adam for Alex, am_michael for
Marc) to keep channel continuity.
"""
import json
import os
import wave
import numpy as np
from pathlib import Path
from kokoro_onnx import Kokoro

ROOT = Path('/home/niko/MindClash')
SCRIPT_PATH = ROOT / 'episodes/EP002_lovins-synthesis/script.json'
SEGMENTS_DIR = ROOT / 'episodes/EP002_lovins-synthesis/audio_segments'
MASTER_PATH = ROOT / 'episodes/EP002_lovins-synthesis/master.wav'

SAMPLE_RATE = 24000  # Kokoro native

print('Loading Kokoro...')
kokoro = Kokoro(ROOT / 'models/kokoro/kokoro-v0_19.onnx',
                 ROOT / 'models/kokoro/voices.bin')
print('OK\n')

# Load script
data = json.loads(SCRIPT_PATH.read_text())
segments = data['segments']
print(f'Script has {len(segments)} segments')

# Voice mapping (same as EP001)
voice_map = {'host': 'am_adam', 'expert': 'am_michael'}

# Generate each segment
SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)
all_audio = []  # master concat
total_duration_est = 0

for i, seg in enumerate(segments, 1):
    text = seg['text']
    speaker = seg['speaker']
    voice = voice_map[speaker]
    seg_id = seg['id']
    pause_ms = seg.get('pause_after_ms', 600)

    # Generate
    gen = kokoro.create(text, voice=voice, speed=1.0, lang='en-us')
    samples, sr = next(gen)
    samples = np.asarray(samples, dtype=np.int16)
    duration = len(samples) / sr
    total_duration_est += duration + pause_ms / 1000.0

    # Save individual segment
    seg_path = SEGMENTS_DIR / f"seg_{seg_id:02d}_{speaker}.wav"
    with wave.open(str(seg_path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(samples.tobytes())

    # Add to master with pause
    all_audio.append(samples)
    pause_samples = int(SAMPLE_RATE * (pause_ms / 1000.0))
    all_audio.append(np.zeros(pause_samples, dtype=np.int16))

    print(f'  [{i:2d}/{len(segments)}] {speaker:6s} {voice} ({seg.get("emotion","?"):14s}) {duration:.1f}s + {pause_ms}ms')

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
