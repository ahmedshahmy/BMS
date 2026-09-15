#!/usr/bin/env python3
"""Build the BMS newsletter site assets and manifests.

For every issue in ``tools/content.py`` this script creates::

    issues/<issue-slug>/
        cover.jpg              <- issue cover for the title screen
        issue.js               <- manifest read by the site (generated)
        <tile-slug>/
            photo.jpg          <- hero image / video poster
            video.mp4          <- short clip (H.264, plays on iOS + Android)
            text.md            <- the article body (source of truth)

Run ``python3 tools/build.py`` after editing content, then commit.

Media is only generated when it is missing, so a real photograph dropped into a
tile folder is never overwritten by a rebuild.

  --skip-media   rewrite only text.md and the manifests (used by CI)
  --force-media  regenerate every placeholder photo and clip
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import ISSUES, SITE  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ISSUES_DIR = ROOT / "issues"

# Brand palette sampled from logo.png
NAVY_DEEP = (1, 13, 48)
NAVY = (1, 35, 125)
NAVY_LIGHT = (18, 62, 168)
RED = (208, 20, 43)
RED_LIGHT = (240, 92, 112)
WHITE = (255, 255, 255)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

PHOTO_W, PHOTO_H = 1280, 720
VIDEO_SECONDS = 5


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    """Greedy word wrap measured against the real font metrics."""
    words, lines, line = text.split(), [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if draw.textlength(candidate, font=fnt) <= max_width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit_title(draw, text: str, max_width: int, max_lines: int = 3,
              start: int = 80, minimum: int = 44):
    """Pick the largest font size where the title wraps inside the box."""
    size = start
    while size > minimum:
        fnt = font(FONT_BOLD, size)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines and all(
            draw.textlength(ln, font=fnt) <= max_width for ln in lines
        ):
            return fnt, lines
        size -= 4
    fnt = font(FONT_BOLD, minimum)
    return fnt, wrap(draw, text, fnt, max_width)


def vertical_gradient(size, top, bottom) -> Image.Image:
    w, h = size
    grad = Image.new("RGB", (1, h))
    px = grad.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        # ease so the deep navy sits mostly at the bottom
        t = t ** 0.85
        px[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return grad.resize((w, h), Image.BILINEAR)


def star_pattern(size, spacing=170, radius=66) -> Image.Image:
    """Faint khatam (8-point star) tessellation used as a background motif."""
    w, h = size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    stroke = (120, 165, 255, 26)
    r2 = radius / math.sqrt(2)
    row = 0
    y = -radius
    while y < h + radius:
        offset = spacing / 2 if row % 2 else 0
        x = -radius + offset
        while x < w + radius:
            d.polygon(
                [(x - r2, y - r2), (x + r2, y - r2), (x + r2, y + r2), (x - r2, y + r2)],
                outline=stroke, width=2,
            )
            d.polygon(
                [(x, y - radius), (x + radius, y), (x, y + radius), (x - radius, y)],
                outline=stroke, width=2,
            )
            x += spacing
        y += spacing
        row += 1
    return layer


def logo_chip(size: int = 116, pad: int = 10) -> Image.Image:
    """The BMS logo on a white rounded card so it reads on a dark photo."""
    logo = Image.open(ROOT / "logo.png").convert("RGBA")
    logo = logo.resize((size - pad * 2, size - pad * 2), Image.LANCZOS)
    chip = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(chip)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=26, fill=(255, 255, 255, 245))
    chip.alpha_composite(logo, (pad, pad))
    return chip


_emoji_cache: dict[int, Image.Image | None] = {}


def emoji_image(char: str, size: int) -> Image.Image | None:
    """Render a colour emoji offscreen; returns None when unavailable."""
    if size in _emoji_cache:
        return _emoji_cache[size]
    img = None
    try:
        # NotoColorEmoji is a bitmap font: it only renders at its strike size.
        base = ImageFont.truetype(FONT_EMOJI, 109)
        canvas = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(canvas).text((20, 20), char, font=base, embedded_color=True)
        bbox = canvas.getbbox()
        if bbox:
            canvas = canvas.crop(bbox)
            ratio = size / max(canvas.width, canvas.height)
            img = canvas.resize(
                (max(1, round(canvas.width * ratio)), max(1, round(canvas.height * ratio))),
                Image.LANCZOS,
            )
    except Exception:  # pragma: no cover - font missing or unsupported
        img = None
    _emoji_cache[size] = img
    return img


# --------------------------------------------------------------------------
# photo + video
# --------------------------------------------------------------------------

def render_photo(issue: dict, tile: dict, out: Path) -> None:
    img = vertical_gradient((PHOTO_W, PHOTO_H), NAVY_LIGHT, NAVY_DEEP).convert("RGBA")
    img.alpha_composite(star_pattern((PHOTO_W, PHOTO_H)))

    # soft red glow bottom-left, brand stripe along the bottom edge
    glow = Image.new("RGBA", (PHOTO_W, PHOTO_H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse(
        [-380, PHOTO_H - 300, 620, PHOTO_H + 340], fill=(*RED, 118)
    )
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(110)))

    # legibility scrim (built as a 1px column, then stretched across)
    alpha = Image.new("L", (1, PHOTO_H))
    ap = alpha.load()
    for y in range(PHOTO_H):
        t = max(0.0, (y - PHOTO_H * 0.30) / (PHOTO_H * 0.70))
        ap[0, y] = int(155 * (t ** 1.5))
    scrim = Image.new("RGBA", (PHOTO_W, PHOTO_H), (2, 8, 30, 0))
    scrim.putalpha(alpha.resize((PHOTO_W, PHOTO_H), Image.BILINEAR))
    img.alpha_composite(scrim)

    d = ImageDraw.Draw(img)
    pad = 72

    img.alpha_composite(logo_chip(), (PHOTO_W - pad - 116, pad))

    emoji = emoji_image(tile["icon"], 78)
    if emoji:
        img.alpha_composite(emoji, (pad, pad + 8))

    eyebrow = f"{issue['edition'].upper()}   \u00b7   ISSUE {issue['number']}"
    d.text((pad, pad + 104), eyebrow, font=font(FONT_BOLD, 26), fill=(*RED_LIGHT, 255))

    text_w = int(PHOTO_W * 0.70)
    fnt, lines = fit_title(d, tile["title"], text_w)
    line_h = round(fnt.size * 1.16)
    total = len(lines) * line_h
    blurb_lines = wrap(d, tile["blurb"], font(FONT_REG, 30), text_w)[:2]
    blurb_h = len(blurb_lines) * 42

    block_h = total + 26 + 6 + 24 + blurb_h
    y = PHOTO_H - pad - block_h

    for line in lines:
        d.text((pad, y), line, font=fnt, fill=(*WHITE, 255))
        y += line_h
    y += 26
    d.rectangle([pad, y, pad + 96, y + 8], fill=(*RED, 255))
    y += 30
    for line in blurb_lines:
        d.text((pad, y), line, font=font(FONT_REG, 30), fill=(226, 233, 250, 255))
        y += 42

    d.rectangle([0, PHOTO_H - 10, PHOTO_W, PHOTO_H], fill=(*RED, 255))

    img.convert("RGB").save(out, "JPEG", quality=82, optimize=True, progressive=True)


def find_ffmpeg() -> str | None:
    local = ROOT / ".buildtools" / "imageio_ffmpeg" / "binaries"
    if local.is_dir():
        for candidate in sorted(local.glob("ffmpeg-*")):
            if os.access(candidate, os.X_OK):
                return str(candidate)
    return shutil.which("ffmpeg")


def render_video(ffmpeg: str, photo: Path, out: Path) -> None:
    """Slow Ken Burns push over the tile photo, encoded as H.264 MP4."""
    frames = VIDEO_SECONDS * 24
    vf = (
        "scale=1760:990,"
        f"zoompan=z='min(1.0+0.00075*on,1.14)':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={frames}:s={PHOTO_W}x{PHOTO_H}:fps=24,"
        "fade=t=in:st=0:d=0.45,"
        f"fade=t=out:st={VIDEO_SECONDS - 0.9}:d=0.9,"
        "format=yuv420p"
    )
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(photo),
        "-vf", vf,
        "-frames:v", str(frames),
        "-c:v", "libx264", "-preset", "slow", "-crf", "31",
        "-profile:v", "high", "-level", "3.1",
        "-movflags", "+faststart", "-an",
        str(out),
    ]
    subprocess.run(cmd, check=True)


# --------------------------------------------------------------------------
# manifests
# --------------------------------------------------------------------------

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_issue_manifest(issue: dict, tiles: list[dict]) -> Path:
    payload = {
        "slug": issue["slug"],
        "number": issue["number"],
        "edition": issue["edition"],
        "title": issue["title"],
        "published": issue["published"],
        "dateLabel": issue["date_label"],
        "summary": issue["summary"],
        "cover": rel(ISSUES_DIR / issue["slug"] / "cover.jpg"),
        "tiles": tiles,
    }
    path = ISSUES_DIR / issue["slug"] / "issue.js"
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    path.write_text(
        "/* Generated by tools/build.py -- do not edit by hand. */\n"
        "window.BMS_ISSUE_DATA = window.BMS_ISSUE_DATA || {};\n"
        f"window.BMS_ISSUE_DATA[{json.dumps(issue['slug'])}] = {body};\n",
        encoding="utf-8",
    )
    return path


def write_catalog(issues: list[dict]) -> Path:
    catalog = [
        {
            "slug": i["slug"],
            "number": i["number"],
            "edition": i["edition"],
            "title": i["title"],
            "published": i["published"],
            "dateLabel": i["date_label"],
            "summary": i["summary"],
            "cover": rel(ISSUES_DIR / i["slug"] / "cover.jpg"),
            "tileCount": len(i["tiles"]),
        }
        for i in issues
    ]
    path = ISSUES_DIR / "index.js"
    body = json.dumps(catalog, ensure_ascii=False, indent=2)
    path.write_text(
        "/* Generated by tools/build.py -- do not edit by hand. */\n"
        f"window.BMS_ISSUES = {body};\n",
        encoding="utf-8",
    )
    return path


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skip-media", action="store_true",
                    help="only rewrite text.md and the manifests")
    ap.add_argument("--force-media", action="store_true",
                    help="regenerate placeholder photos and clips even if present")
    args = ap.parse_args()

    ISSUES_DIR.mkdir(parents=True, exist_ok=True)
    want_media = not args.skip_media
    ffmpeg = find_ffmpeg() if want_media else None
    if want_media and not ffmpeg:
        print("! ffmpeg not found - skipping video encoding", file=sys.stderr)

    def needs(path: Path) -> bool:
        """Generate media only when it is absent, so real photos survive."""
        return want_media and (args.force_media or not path.exists())

    for issue in ISSUES:
        issue_dir = ISSUES_DIR / issue["slug"]
        issue_dir.mkdir(parents=True, exist_ok=True)
        tiles_out = []

        for tile in issue["tiles"]:
            tdir = issue_dir / tile["slug"]
            tdir.mkdir(parents=True, exist_ok=True)

            (tdir / "text.md").write_text(
                tile["text"].strip() + "\n", encoding="utf-8"
            )

            photo = tdir / "photo.jpg"
            video = tdir / "video.mp4"
            if needs(photo):
                render_photo(issue, tile, photo)
            if needs(video) and ffmpeg:
                render_video(ffmpeg, photo, video)

            tiles_out.append({
                "slug": tile["slug"],
                "title": tile["title"],
                "icon": tile["icon"],
                "blurb": tile["blurb"],
                "photo": rel(photo),
                "video": rel(video) if video.exists() else None,
                "textFile": rel(tdir / "text.md"),
                "text": tile["text"].strip(),
            })
            print(f"  {issue['slug']}/{tile['slug']}")

        write_issue_manifest(issue, tiles_out)

        cover = issue_dir / "cover.jpg"
        if needs(cover):
            render_cover(issue, cover)

        print(f"\u2713 {issue['slug']}  ({len(tiles_out)} tiles)")

    write_catalog(ISSUES)
    print(f"\n\u2713 {len(ISSUES)} issues written to {rel(ISSUES_DIR)}/")
    return 0


def render_cover(issue: dict, out: Path) -> None:
    """Wide banner for the title screen / archive cards."""
    w, h = 1280, 560
    img = vertical_gradient((w, h), NAVY, NAVY_DEEP).convert("RGBA")
    img.alpha_composite(star_pattern((w, h), spacing=150, radius=58))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([w - 620, -320, w + 320, 320], fill=(*RED, 130))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))

    d = ImageDraw.Draw(img)
    pad = 76
    img.alpha_composite(logo_chip(128), (w - pad - 128, pad))

    d.text((pad, pad + 10), f"ISSUE {issue['number']}", font=font(FONT_BOLD, 30),
           fill=(*RED_LIGHT, 255))
    fnt, lines = fit_title(d, issue["edition"], int(w * 0.62), max_lines=2,
                           start=92, minimum=52)
    y = pad + 66
    for line in lines:
        d.text((pad, y), line, font=fnt, fill=(*WHITE, 255))
        y += round(fnt.size * 1.14)
    d.rectangle([pad, y + 14, pad + 110, y + 22], fill=(*RED, 255))
    d.text((pad, y + 44), issue["date_label"], font=font(FONT_REG, 32),
           fill=(222, 230, 248, 255))
    d.rectangle([0, h - 10, w, h], fill=(*RED, 255))

    img.convert("RGB").save(out, "JPEG", quality=84, optimize=True, progressive=True)


if __name__ == "__main__":
    raise SystemExit(main())
