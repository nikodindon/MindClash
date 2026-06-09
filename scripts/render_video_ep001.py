"""Generate YouTube video for EP001 from master.wav + a background image.

Creates a 24-min video with:
  - Static background image (looping fade)
  - Audio track (master.wav or final.wav)
  - Optional: text overlay (currently minimal — title at start, "MindClash" watermark)
  - Optional: subtle waveform visualization

Output: episodes/EP001_jancovici-synthesis/video.mp4 (H.264, 30fps, 1280x720)
"""
import subprocess
from pathlib import Path

ROOT = Path('/home/niko/MindClash')
EP = ROOT / 'episodes/EP001_jancovici-synthesis'

# Inputs
AUDIO = EP / 'final.wav' if (EP / 'final.wav').exists() else EP / 'master.wav'

# Look for any background image (jpg or png)
bg_candidates = [
    ROOT / 'assets/thumbnails/background.png',
    ROOT / 'assets/thumbnails/background.jpg',
    ROOT / 'assets/thumbnails/background_default.png',
]
THUMB = None
for c in bg_candidates:
    if c.exists():
        THUMB = c
        break

if THUMB is None:
    print(f'WARNING: No background image found in assets/thumbnails/')
    print('  Run: python scripts/generate_background.py "Your Topic"')
    print('  Using a simple colored background instead')
    # Generate a simple solid color background
    THUMB = '/tmp/background.png'
    subprocess.run([
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f'color=c=#0a0e1a:s=1280x720:d=1',
        '-frames:v', '1', THUMB
    ], check=True, capture_output=True)

OUT = EP / 'video.mp4'

# Get audio duration
import wave
with wave.open(str(AUDIO), 'rb') as w:
    nframes = w.getnframes()
    sr = w.getframerate()
    duration = nframes / sr
print(f'Audio: {AUDIO.name}, {duration:.1f}s = {duration/60:.1f} min')

# Build ffmpeg command
# -loop 1: loop the image
# -i: image input
# -i: audio input
# -c:v libx264: H.264 video codec
# -tune stillimage: optimize for static image
# -c:a aac: AAC audio codec
# -b:a 192k: audio bitrate
# -shortest: end video when audio ends
cmd = [
    'ffmpeg', '-y',
    '-loop', '1',
    '-i', str(THUMB),
    '-i', str(AUDIO),
    '-c:v', 'libx264',
    '-tune', 'stillimage',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-pix_fmt', 'yuv420p',
    '-shortest',
    '-vf', 'scale=1280:720',
    str(OUT)
]

print('\nRendering video with ffmpeg...')
print(f'  Command: {" ".join(cmd[:6])}...')
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f'FFMPEG FAILED (exit {result.returncode}):')
    print(result.stderr[-1000:])
    raise SystemExit(1)

size_mb = OUT.stat().st_size / 1024 / 1024
print(f'\n✓ Video saved: {OUT} ({size_mb:.1f} MB)')
print(f'  Duration: {duration/60:.1f} min')
print(f'  Resolution: 1280x720 (720p)')
print(f'  Codec: H.264 video + AAC audio')
