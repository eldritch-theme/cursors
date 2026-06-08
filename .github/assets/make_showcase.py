import os
import sys
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

# Path needs to be result link from nix build
RESULT = Path("/home/neonvoid/dev/cursors/result/share/icons")
OUTPUT = Path("./cursors.png")

PALETTE_LABELS = {
    "great-old-green": "Great Old Green",
    "watery-tomb-blue": "Watery Tomb Blue",
    "pustule-pink": "Pustule Pink",
    "lovecraft-purple": "Lovecraft Purple",
    "rlyeh-red": "R'lyeh Red",
    "dreaming-orange": "Dreaming Orange",
    "gold-of-yuggoth": "Gold of Yuggoth",
    "sunken-depths": "Sunken Depths",
    "lighthouse-white": "Lighthouse White",
}

CURSOR_TYPES = [
    "default",
    "pointer",
    "text",
    "crosshair",
    "openhand",
    "pencil",
    "no-drop",
    "help",
    "zoom-in",
    "color-picker",
    "all-scroll",
    "progress",
]

ACCENT_NAMES = list(PALETTE_LABELS.keys())

CELL = 96
PAD = 12
HEADER_H = 40
LABEL_W = 170
MARGIN = 20

COLS = len(CURSOR_TYPES)
ROWS = len(ACCENT_NAMES)

W = MARGIN * 2 + LABEL_W + COLS * CELL + (COLS - 1) * PAD
H = MARGIN * 2 + HEADER_H + ROWS * CELL + (ROWS - 1) * PAD

BG = (26, 27, 46)
TEXT_COLOR = (235, 250, 250)

import subprocess


def find_font(name):
    result = subprocess.run(
        ["fc-list", "-f", "%{file}", "--family", name],
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().split("\n")[0]
    return None


font_path = find_font("NeonMono")
bold_path = find_font("NeonMono:style=Bold")
if not bold_path:
    bold_path = find_font("NeonMono") and font_path  # fallback

try:
    FONT = ImageFont.truetype(bold_path or font_path, 14)
    FONT_SM = ImageFont.truetype(font_path, 11)
except Exception:
    FONT = ImageFont.load_default()
    FONT_SM = FONT


def render_svg(svg_path):
    try:
        png_data = cairosvg.svg2png(
            url=str(svg_path), output_width=CELL, output_height=CELL
        )
        img = Image.open(io.BytesIO(png_data)).convert("RGBA")
        if img.size != (CELL, CELL):
            img = img.resize((CELL, CELL), Image.LANCZOS)
        return img
    except Exception as e:
        print(f"  FAILED: {svg_path.name}: {e}", file=sys.stderr)
        return None


import io


def main():
    img = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Column headers
    for ci, cname in enumerate(CURSOR_TYPES):
        x = MARGIN + LABEL_W + PAD + ci * (CELL + PAD)
        _, _, tw, _ = draw.textbbox((0, 0), cname, font=FONT_SM)
        draw.text(
            (x + CELL // 2 - tw // 2, MARGIN + 10), cname, fill=TEXT_COLOR, font=FONT_SM
        )

    # Row labels
    for ri, accent in enumerate(ACCENT_NAMES):
        label = PALETTE_LABELS[accent]
        y = MARGIN + HEADER_H + PAD + ri * (CELL + PAD)
        _, _, tw, th = draw.textbbox((0, 0), label, font=FONT)
        draw.text(
            (MARGIN + LABEL_W - tw - 8, y + CELL // 2 - th // 2),
            label,
            fill=TEXT_COLOR,
            font=FONT,
        )

    # Cursor cells
    for ri, accent in enumerate(ACCENT_NAMES):
        theme_dir = RESULT / f"eldritch-{accent}-cursors" / "cursors_scalable"
        if not theme_dir.exists():
            print(f"SKIP: {theme_dir} not found", file=sys.stderr)
            continue

        for ci, cname in enumerate(CURSOR_TYPES):
            dir_path = theme_dir / cname
            svg_path = dir_path / f"{cname}.svg"
            if not svg_path.exists():
                svgs = list(dir_path.glob("*.svg"))
                if svgs:
                    svg_path = svgs[0]
                else:
                    print(f"  missing: {cname} in {theme_dir.name}", file=sys.stderr)
                    continue

            cursor_img = render_svg(svg_path)
            if cursor_img is None:
                continue

            x = MARGIN + LABEL_W + PAD + ci * (CELL + PAD)
            y = MARGIN + HEADER_H + PAD + ri * (CELL + PAD)
            img.paste(cursor_img, (x, y), cursor_img)

    img.save(OUTPUT, "PNG")
    print(f"Saved {OUTPUT} ({W}x{H})")


if __name__ == "__main__":
    main()
