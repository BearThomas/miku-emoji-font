#!/usr/bin/env python3
"""Build a CBDT/CBLC color-bitmap emoji font from PNG artwork.

Usage:
    python3 build_font.py --art art/ --subset build/subset.ttf \
        --manifest art/manifest.json --family "Miku Emoji" --out build/MikuEmoji.ttf

The subset must be a valid CBDT font covering the wanted codepoints, e.g.:
    pyftsubset /usr/share/fonts/apple-color-emoji/apple-color-emoji.ttf \
        --unicodes=U+1F602,U+1F62D --output-file=build/subset.ttf

We reuse that container (instead of hand-rolling CBLC/CBDT blobs) because
FreeType rejects subtly malformed tables with an opaque "broken file".
"""
import os, io, json, argparse
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.C_B_D_T_ import SmallGlyphMetrics


def normalize(src, size=1024, pad=0.04):
    im = Image.open(src).convert("RGBA")
    bb = im.getbbox()
    if bb:
        im = im.crop(bb)
    art = int(size * (1 - 2 * pad))
    im = im.resize((art, art), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    off = (size - art) // 2
    canvas.paste(im, (off, off), im)
    return canvas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--art", required=True, help="folder with the source PNGs")
    ap.add_argument("--manifest", required=True, help="JSON: {\"01_laugh.png\": \"U+1F602\", ...}")
    ap.add_argument("--subset", required=True, help="valid CBDT font covering the codepoints")
    ap.add_argument("--family", required=True, help="font family name, e.g. 'Miku Emoji'")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pad", type=float, default=0.04)
    ap.add_argument("--scale", type=float, default=1.0,
                    help="glyph size multiplier, >1 makes emoji bigger than 1em (Noto uses ~1.25)")
    ap.add_argument("--bearing", type=float, default=0.85,
                    help="bitmap top above baseline, as a fraction of ppem")
    args = ap.parse_args()

    manifest = json.load(open(args.manifest))
    codes = {k: int(v[2:], 16) if isinstance(v, str) else int(v) for k, v in manifest.items()}

    font = TTFont(args.subset)
    cmap = font.getBestCmap()

    for rec in font["name"].names:
        rec.string = rec.toUnicode()  # no-op, keeps records valid
    for nid, value in ((1, args.family), (2, "Regular"), (3, f"{args.family} 1.0"),
                       (4, f"{args.family} Regular"), (6, args.family.replace(" ", "") + "-Regular")):
        font["name"].setName(value, nid, 3, 1, 0x409)
        font["name"].setName(value, nid, 1, 0, 0)

    cbdt, cblc = font["CBDT"], font["CBLC"]
    done = 0
    for idx, strike in enumerate(cblc.strikes):
        bst = strike.bitmapSizeTable
        px, py = bst.ppemX, bst.ppemY
        glyphs = cbdt.strikeData[idx]
        for fname, cp in codes.items():
            gname = cmap.get(cp)
            src = os.path.join(args.art, fname)
            if not gname or gname not in glyphs or not os.path.exists(src):
                continue
            w, h = round(px * args.scale), round(py * args.scale)
            im = normalize(src, pad=args.pad).resize((w, h), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format="PNG", optimize=True)
            gl = glyphs[gname]
            gl.imageData = buf.getvalue()
            m = SmallGlyphMetrics()
            m.height = h
            m.width = w
            m.BearingX = 0
            m.BearingY = min(round(h * args.bearing), 127)
            m.Advance = w
            gl.metrics = m
            done += 1

    font.save(args.out)
    print(f"wrote {args.out} ({os.path.getsize(args.out)} bytes), {done} glyph bitmaps updated, "
          f"{len(cblc.strikes)} strikes")


if __name__ == "__main__":
    main()
