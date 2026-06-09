"""Mix the EP001 master.wav with intro/outro music + section stings.

Inputs:
  - episodes/EP001_jancovici-synthesis/master.wav (24 min, Kokoro TTS)
  - assets/music/intro.wav (optional, 10s ambient fade in)
  - assets/music/outro.wav (optional, 15s ambient fade out)
  - assets/music/sting.wav (optional, 2s ambient sting)

Output:
  - episodes/EP001_jancovici-synthesis/final.wav (with music bed)
"""
import wave
import os
import numpy as np
from pathlib import Path

ROOT = Path('/home/niko/MindClash')
EP = ROOT / 'episodes/EP001_jancovici-synthesis'
MASTER = EP / 'master.wav'
OUT = EP / 'final.wav'

SAMPLE_RATE = 24000  # Match Kokoro output


def load_wav_or_silent(path, duration_s, n_channels=1, sample_width=2):
    """Load a wav file, or generate silence if missing."""
    if not path.exists():
        return np.zeros(int(duration_s * SAMPLE_RATE), dtype='int16')
    with wave.open(str(path), 'rb') as w:
        nch = w.getnchannels()
        sw = w.getsampwidth()
        sr = w.getframerate()
        nframes = w.getnframes()
        data = w.readframes(nframes)
    if sr != SAMPLE_RATE:
        print(f'  WARNING: {path.name} has sr={sr}, expected {SAMPLE_RATE}')
    if sw != 2:
        data = np.frombuffer(data, dtype='uint8').repeat(2).tobytes()  # rough upsample
    audio = np.frombuffer(data, dtype='int16')
    if nch > 1:
        audio = audio[::nch]  # take left channel
    return audio


def fade_in(audio, duration_s=2.0):
    n = int(duration_s * SAMPLE_RATE)
    n = min(n, len(audio))
    audio = audio.copy()
    audio[:n] = (audio[:n].astype(np.float32) * np.linspace(0, 1, n)).astype(np.int16)
    return audio


def fade_out(audio, duration_s=3.0):
    n = int(duration_s * SAMPLE_RATE)
    n = min(n, len(audio))
    audio = audio.copy()
    audio[-n:] = (audio[-n:].astype(np.float32) * np.linspace(1, 0, n)).astype(np.int16)
    return audio


# Load master
print(f'Loading master: {MASTER}')
with wave.open(str(MASTER), 'rb') as w:
    nch = w.getnchannels()
    sw = w.getsampwidth()
    sr = w.getframerate()
    nframes = w.getnframes()
    master_data = w.readframes(nframes)
print(f'  {nframes} samples, {nframes/sr:.1f}s, {nch}ch, {sw*8}-bit')
master = np.frombuffer(master_data, dtype='int16')
if nch > 1:
    master = master[::nch]

# Load music beds (or generate silence)
print(f'Loading intro music: {ROOT}/assets/music/intro.wav')
intro = load_wav_or_silent(ROOT / 'assets/music/intro.wav', 10.0)

print(f'Loading outro music: {ROOT}/assets/music/outro.wav')
outro = load_wav_or_silent(ROOT / 'assets/music/outro.wav', 15.0)

print(f'Loading section sting: {ROOT}/assets/music/sting.wav')
sting = load_wav_or_silent(ROOT / 'assets/music/sting.wav', 2.0)

# Apply fades to music
intro = fade_in(intro, 2.0)
outro = fade_out(outro, 3.0)

# Mix: intro (10s) + master (24 min) + outro (15s) = ~24.5 min
print('\nMixing...')
mixed = np.concatenate([intro, master, outro])
print(f'  Final: {len(mixed)} samples, {len(mixed)/SAMPLE_RATE:.1f}s = {len(mixed)/SAMPLE_RATE/60:.1f} min')

# Write final
with wave.open(str(OUT), 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SAMPLE_RATE)
    w.writeframes(mixed.tobytes())

size_mb = OUT.stat().st_size / 1024 / 1024
print(f'\n✓ Final saved: {OUT} ({size_mb:.1f} MB)')

# Optional: also export to MP3 if ffmpeg is available
import subprocess
try:
    mp3_out = OUT.with_suffix('.mp3')
    subprocess.run(
        ['ffmpeg', '-y', '-i', str(OUT), '-codec:a', 'libmp3lame', '-b:a', '192k', str(mp3_out)],
        check=True, capture_output=True
    )
    print(f'✓ MP3 saved: {mp3_out} ({mp3_out.stat().st_size/1024/1024:.1f} MB)')
except (subprocess.CalledProcessError, FileNotFoundError) as e:
    print(f'  MP3 export skipped: {e}')
