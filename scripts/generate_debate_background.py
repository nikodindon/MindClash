"""
Generate a YouTube-friendly background image for MindClash DEBATES.

Unlike generate_background.py (which is for solo podcasts with orange
accent), this one is for the 1-on-1 debate format with:
  - Dark blue (not orange) background — visually differentiates the
    "debate" mode from the "solo podcast" mode on the channel
  - Two protagonist photos side-by-side (left/right)
  - "DEBATE NUMBER N" label at the top
  - "VS" in the center between the two photos
  - Name of each protagonist under their photo
  - MindClash branding

Usage:
  python scripts/generate_debate_background.py \
      --left /path/to/janco.png \
      --right /path/to/lovins.png \
      --name-left "Jean-Marc Jancovici" \
      --name-right "Amory Lovins" \
      --number 1 \
      --out episodes/EP003_jancovici-vs-lovins/background.png
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# === Debate-mode colors (cool blue, NOT orange) ===
BG_TOP = (8, 14, 36)         # very dark navy blue
BG_BOTTOM = (2, 4, 16)       # near-black blue
ACCENT = (90, 150, 255)      # cool blue (debate accent)
TEXT = (220, 220, 230)       # light cool gray
TEXT_DIM = (140, 145, 165)   # medium cool gray
ACCENT_WARM = (255, 200, 80) # warm gold for the "DEBATE NUMBER" callout (subtle contrast)

W, H = 1280, 720


def make_vertical_gradient(w: int, h: int, top_color, bottom_color) -> Image.Image:
    img = Image.new('RGB', (w, h), bottom_color)
    pixels = img.load()
    for y in range(h):
        ratio = y / h
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        for x in range(w):
            pixels[x, y] = (r, g, b)
    return img


def add_radial_glow(img: Image.Image, color, max_radius: int = 250) -> Image.Image:
    """Subtle blue radial glow behind the center."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    w, h = img.size
    for r in range(max_radius, 0, -10):
        alpha = int(15 * (1 - r / max_radius))
        od.ellipse([w//2 - r*2, -r, w//2 + r*2, r*2], fill=(*color, alpha))
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')


def harmonize_photo(src_path: Path, target_size: int) -> Image.Image:
    """Load a portrait photo, crop to a square centered on the face area,
    resize to target_size, convert to RGB. If the image isn't a clean
    portrait, just do a center crop."""
    im = Image.open(src_path).convert('RGBA')
    w, h = im.size
    # Center-crop to square
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    im = im.crop((left, top, left + side, top + side))
    # Resize
    im = im.resize((target_size, target_size), Image.LANCZOS)
    # Composite onto a dark blue square (to handle transparency)
    bg = Image.new('RGBA', im.size, (*BG_BOTTOM, 255))
    im = Image.alpha_composite(bg, im).convert('RGB')
    # Subtle blue tint boost
    return im


def add_circular_border(img: Image.Image, color, border_width: int = 4) -> Image.Image:
    """Add a thin colored circle border around the image (looks like a
    circular portrait frame)."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    w, h = img.size
    od.ellipse([(0, 0), (w, h)], outline=(*color, 255), width=border_width)
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')


def draw_centered(draw: ImageDraw.Draw, text: str, y: int, font, color, w: int):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(((w - text_w) / 2, y), text, font=font, fill=color)


def find_font(size: int):
    """Try to find a usable system font, fall back to default."""
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/TTF/DejaVuSans.ttf',
    ]
    for fp in font_paths:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def main():
    parser = argparse.ArgumentParser(description="Generate MindClash debate background image")
    parser.add_argument("--left", required=True, help="Path to left protagonist photo (PNG/JPG)")
    parser.add_argument("--right", required=True, help="Path to right protagonist photo (PNG/JPG)")
    parser.add_argument("--name-left", required=True, help="Name of left protagonist")
    parser.add_argument("--name-right", required=True, help="Name of right protagonist")
    parser.add_argument("--number", type=int, default=1, help="Debate number (1, 2, 3...)")
    parser.add_argument("--out", default="background.png", help="Output PNG path")
    args = parser.parse_args()

    # Photo dimensions: each will be 280x280, positioned on the sides
    PHOTO_SIZE = 280
    LEFT_X = 180
    RIGHT_X = W - LEFT_X - PHOTO_SIZE
    PHOTO_Y = 280  # vertical center-ish

    print(f'Generating debate #{args.number} background ({W}x{H})')
    print(f'  Left: {args.name_left} <- {args.left}')
    print(f'  Right: {args.name_right} <- {args.right}')

    # Base gradient
    img = make_vertical_gradient(W, H, BG_TOP, BG_BOTTOM)
    img = add_radial_glow(img, ACCENT)
    draw = ImageDraw.Draw(img)

    # Fonts
    font_branding = find_font(36)        # MINDCLASH top
    font_debate_label = find_font(48)    # "DEBATE NUMBER 1"
    font_vs = find_font(110)            # "VS" center
    font_name = find_font(28)           # names under photos
    font_disclaimer = find_font(18)     # bottom

    # Top: MINDCLASH branding in cool blue
    draw_centered(draw, "MINDCLASH", 45, font_branding, ACCENT, W)

    # "DEBATE NUMBER N" (the gold callout)
    debate_label = f"DEBATE NUMBER {args.number}"
    draw_centered(draw, debate_label, 110, font_debate_label, ACCENT_WARM, W)

    # Subtle horizontal line under the label
    draw.line([(0, 180), (W, 180)], fill=(*ACCENT, 120), width=2)

    # Process & place left photo
    left_im = harmonize_photo(Path(args.left), PHOTO_SIZE)
    left_im = add_circular_border(left_im, ACCENT, border_width=4)
    img.paste(left_im, (LEFT_X, PHOTO_Y))

    # Right photo
    right_im = harmonize_photo(Path(args.right), PHOTO_SIZE)
    right_im = add_circular_border(right_im, ACCENT, border_width=4)
    img.paste(right_im, (RIGHT_X, PHOTO_Y))

    # "VS" in the center
    draw_centered(draw, "VS", PHOTO_Y + PHOTO_SIZE//2 - 60, font_vs, ACCENT, W)

    # Names under each photo (small, dim)
    name_y = PHOTO_Y + PHOTO_SIZE + 20
    bbox_l = draw.textbbox((0, 0), args.name_left, font=font_name)
    text_w_l = bbox_l[2] - bbox_l[0]
    draw.text((LEFT_X + (PHOTO_SIZE - text_w_l) // 2, name_y), args.name_left, font=font_name, fill=TEXT)

    bbox_r = draw.textbbox((0, 0), args.name_right, font=font_name)
    text_w_r = bbox_r[2] - bbox_r[0]
    draw.text((RIGHT_X + (PHOTO_SIZE - text_w_r) // 2, name_y), args.name_right, font=font_name, fill=TEXT)

    # AI disclaimer at bottom
    draw_centered(draw, "AI-assisted debate · Source-grounded · Arena format",
                  H - 50, font_disclaimer, TEXT_DIM, W)

    # Subtle bottom line
    draw.line([(0, H - 80), (W, H - 80)], fill=(*ACCENT, 120), width=2)

    # Save
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, 'PNG', optimize=True)
    print(f'  → {out} ({out.stat().st_size/1024:.0f} KB)')


if __name__ == "__main__":
    main()
