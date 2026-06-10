"""
Generate a YouTube-friendly background image for MindClash episodes.

Creates a 1280x720 PNG with:
  - Dark gradient background (deep blue to black)
  - Subtle "MindClash" branding
  - Topic-specific hint (parameterizable)
  - Optional secondary subtitle (e.g. "A podcast on Amory Lovins")
    rendered smaller between the main title and the AI disclaimer
  - No flashy elements (clean, documentary-style)

Usage:
  python scripts/generate_background.py "THE THERMODYNAMICS OF CIVILIZATION"
  python scripts/generate_background.py "THE NEGAWATT REVOLUTION" \
      --subtitle "A podcast on Amory Lovins"
  python scripts/generate_background.py "MY TITLE" --out /tmp/my_bg.png
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Colors
BG_TOP = (10, 14, 26)        # very dark blue
BG_BOTTOM = (0, 0, 0)        # black
ACCENT = (255, 90, 50)       # warm orange-red
TEXT = (220, 220, 220)       # light gray
TEXT_DIM = (140, 140, 140)   # medium gray
TEXT_SUB = (170, 170, 170)   # medium gray (between TEXT and TEXT_DIM)

W, H = 1280, 720
OUT = Path('/home/niko/MindClash/assets/thumbnails/background_default.png')
OUT.parent.mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser(description="Generate MindClash background image")
parser.add_argument("topic", nargs="?",
                    default="ENERGY · CLIMATE · CIVILIZATION",
                    help="Main title text (big, centered)")
parser.add_argument("--subtitle", "-s", default=None,
                    help="Optional secondary line below the main title, "
                         "rendered smaller. Use to identify the podcast subject, "
                         "e.g. 'A podcast on Amory Lovins'")
parser.add_argument("--out", "-o", default=None,
                    help="Output PNG path. Default: assets/thumbnails/background_default.png")
args = parser.parse_args()

topic = args.topic
subtitle = args.subtitle
if args.out:
    OUT = Path(args.out)
    OUT.parent.mkdir(parents=True, exist_ok=True)

print(f'Generating background ({W}x{H}) with topic: "{topic}"')
if subtitle:
    print(f'  + subtitle: "{subtitle}"')
print(f'  → {OUT}')

# Create base
img = Image.new('RGB', (W, H), BG_BOTTOM)
draw = ImageDraw.Draw(img)

# Vertical gradient
for y in range(H):
    ratio = y / H
    r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
    g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
    b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Subtle radial glow in center (top half)
for r in range(300, 0, -10):
    alpha = int(20 * (1 - r / 300))
    color = (*ACCENT, alpha)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([W//2 - r*2, -r, W//2 + r*2, r*2], fill=color)
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

# Try to find a font
font_paths = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/TTF/DejaVuSans.ttf',
]
font_big = None
font_med = None
font_small = None
font_sub = None
for fp in font_paths:
    if Path(fp).exists():
        font_big = ImageFont.truetype(fp, 56)
        font_med = ImageFont.truetype(fp, 32)
        font_small = ImageFont.truetype(fp, 18)
        font_sub = ImageFont.truetype(fp, 26)
        break
if not font_big:
    font_big = ImageFont.load_default()
    font_med = font_big
    font_small = font_big
    font_sub = font_big

# Center topic text
def draw_centered(text, y, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((W - w) / 2, y), text, font=font, fill=color)

# Brand "MINDCLASH" top
draw_centered("MINDCLASH", 60, font_med, ACCENT)

# Big topic (centered around H/2)
draw_centered(topic, H // 2 - 80, font_big, TEXT)

# Optional subtitle (smaller, below the main title, before the AI disclaimer)
if subtitle:
    draw_centered(subtitle, H // 2 + 0, font_sub, TEXT_SUB)

# Subtitle at bottom
draw_centered("AI-assisted podcast · Source-grounded analysis", H - 80, font_small, TEXT_DIM)

# Subtle horizontal lines (top + bottom)
draw.line([(0, 120), (W, 120)], fill=ACCENT, width=2)
draw.line([(0, H - 120), (W, H - 120)], fill=ACCENT, width=2)

img.save(OUT, 'PNG', optimize=True)
print(f'✓ Saved: {OUT} ({OUT.stat().st_size/1024:.0f} KB)')
