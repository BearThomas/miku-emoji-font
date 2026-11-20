#!/usr/bin/env python3
"""Build MikuEmoji.ttf by swapping Apple Color Emoji's CBDT bitmaps for our art.

Keeping Apple's (valid, multi-strike) CBDT/CBLC container avoids hand-rolling
the bitmap tables, and FreeType/Qt already know how to render it at any size.
"""
import os, io
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.C_B_D_T_ import SmallGlyphMetrics

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUTDIR = os.path.join(HERE, "out")
PNG = os.path.join(OUTDIR, "png")
os.makedirs(PNG, exist_ok=True)

BASE = 1024
PAD_RATIO = 0.04
BEARING_RATIO = 0.85
SUBSET = os.path.join(OUTDIR, "subset.ttf")
OUT = os.path.join(OUTDIR, "MikuEmoji.ttf")

CODES = {
    "01_laugh": 0x1F602, "02_cry": 0x1F62D, "03_smile": 0x1F60A,
    "04_heart_eyes": 0x1F60D, "05_loving": 0x1F970, "06_angry": 0x1F621,
    "07_sleep": 0x1F634, "08_think": 0x1F914, "09_sweat": 0x1F605,
    "10_thumbs": 0x1F44D, "11_pray": 0x1F64F, "12_green_heart": 0x1F49A,
    "13_headphones": 0x1F3A7, "14_mic": 0x1F3A4, "15_note": 0x1F3B5,
    "16_sparkles": 0x2728,
}


def normalize(src, dst, size=BASE):
    im = Image.open(src).convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    art = int(size * (1 - 2 * PAD_RATIO))
    im = im.resize((art, art), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    off = (size - art) // 2
    canvas.paste(im, (off, off), im)
    canvas.save(dst)


def main():
    stems = [s for s in CODES if os.path.exists(os.path.join(RAW, s + ".png"))]
    missing = [s for s in CODES if s not in stems]
    if missing:
        print("WARNING missing:", ", ".join(missing))
    for s in stems:
        normalize(os.path.join(RAW, s + ".png"), os.path.join(PNG, s + ".png"))

    font = TTFont(SUBSET)
    cmap = font.getBestCmap()
    name_for = {}
    for stem in stems:
        gname = cmap.get(CODES[stem])
        if gname:
            name_for[stem] = gname
        else:
            print("WARNING no glyph for", stem)

    # rename the family so it does not shadow Apple Color Emoji
    for rec in font["name"].names:
        if rec.nameID in (1, 3, 4, 6, 16, 18, 20, 21):
            pass
    font["name"].setName("Miku Emoji", 1, 3, 1, 0x409)
    font["name"].setName("Regular", 2, 3, 1, 0x409)
    font["name"].setName("Miku Emoji Regular 1.0", 3, 3, 1, 0x409)
    font["name"].setName("Miku Emoji Regular", 4, 3, 1, 0x409)
    font["name"].setName("MikuEmoji-Regular", 6, 3, 1, 0x409)

    cbdt = font["CBDT"]
    cblc = font["CBLC"]
    print("strikes:", [(s.bitmapSizeTable.ppemX, s.bitmapSizeTable.ppemY) for s in cblc.strikes])

    for idx, strike in enumerate(cblc.strikes):
        bst = strike.bitmapSizeTable
        ppem_x, ppem_y = bst.ppemX, bst.ppemY
        glyphs = cbdt.strikeData[idx]
        for stem, gname in name_for.items():
            if gname not in glyphs:
                print("  skip", stem, "in strike", ppem_y)
                continue
            im = Image.open(os.path.join(PNG, stem + ".png")).convert("RGBA")
            im = im.resize((ppem_x, ppem_y), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format="PNG", optimize=True)
            g = glyphs[gname]
            g.imageData = buf.getvalue()
            m = SmallGlyphMetrics()
            m.height = ppem_y
            m.width = ppem_x
            m.BearingX = 0
            m.BearingY = min(round(ppem_y * BEARING_RATIO), 127)
            m.Advance = ppem_x
            g.metrics = m

    font.save(OUT)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
