#!/usr/bin/env python3
"""Add new color-bitmap glyphs (with ligatures) to a CBDT/CBLC emoji font.

Strategy: instead of appending index subtables (fragile), rebuild each
strike's CBLC index subtable as ONE format-1 table covering every glyph that
has a bitmap, in glyph-id order. All participating glyphs get a bitmap (the
invisible joiners get a 1x1 transparent PNG), so the offset array is dense.
"""
import io, sys
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.C_B_D_T_ import SmallGlyphMetrics, cbdt_bitmap_format_17
from fontTools.ttLib.tables.E_B_L_C_ import eblc_index_sub_table_1
from fontTools.feaLib.builder import addOpenTypeFeatures

TRANS = None


def blank_png():
    global TRANS
    if TRANS is None:
        buf = io.BytesIO()
        Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(buf, format="PNG")
        TRANS = buf.getvalue()
    return TRANS


def add_cmap(font, cp, gname):
    for t in font["cmap"].tables:
        if not t.isUnicode():
            continue
        if t.format == 4 and cp <= 0xFFFF:
            t.cmap[cp] = gname
        elif t.format == 12:
            t.cmap[cp] = gname


def ensure_glyph(font, gname, advance=1000):
    order = font.getGlyphOrder()
    if gname in order:
        return
    order.append(gname)
    font.setGlyphOrder(order)
    font["hmtx"][gname] = (advance, 0)
    font["maxp"].numGlyphs = len(order)


def put_bitmap(font, gname, im, bearing=0.85):
    """Add/Replace the bitmap of gname in every strike."""
    cbdt, cblc = font["CBDT"], font["CBLC"]
    for i, strike in enumerate(cblc.strikes):
        bst = strike.bitmapSizeTable
        px, py = bst.ppemX, bst.ppemY
        if im is None:
            data = blank_png()
            w, h = 1, 1
        else:
            w, h = px, py
            buf = io.BytesIO()
            im.resize((px, py), Image.LANCZOS).save(buf, format="PNG", optimize=True)
            data = buf.getvalue()
        m = SmallGlyphMetrics()
        m.height, m.width = h, w
        m.BearingX = 0
        m.BearingY = min(round(h * bearing), 127)
        m.Advance = 0 if im is None else px
        g = cbdt_bitmap_format_17(b"", font)
        g.imageData = data
        g.metrics = m
        cbdt.strikeData[i][gname] = g


def rebuild_cblc(font):
    """One index subtable per strike covering all glyphs that have bitmaps."""
    cbdt, cblc = font["CBDT"], font["CBLC"]
    order = font.getGlyphOrder()
    for i, strike in enumerate(cblc.strikes):
        names = [g for g in order[1:] if g in cbdt.strikeData[i]]
        if not names:
            continue
        # names must be in glyph-id order
        names.sort(key=lambda g: order.index(g))
        gids = [order.index(g) for g in names]
        ist = eblc_index_sub_table_1(b"", font)
        ist.indexFormat = 1
        ist.imageFormat = 17
        ist.imageDataOffset = 0
        ist.firstGlyphIndex = gids[0]
        ist.lastGlyphIndex = gids[-1]
        ist.names = names
        strike.indexSubTables = [ist]
        bst = strike.bitmapSizeTable
        bst.startGlyphIndex = gids[0]
        bst.endGlyphIndex = gids[-1]
        bst.numberOfIndexSubTables = 1


def main():
    font = TTFont(sys.argv[1])
    print("glyphs in:", len(font.getGlyphOrder()))
    # --- demo: add a composed glyph for 😵‍💫 ---
    im = Image.open(sys.argv[2]).convert("RGBA")
    bb = im.getbbox()
    if bb:
        im = im.crop(bb)
    side = max(im.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)

    base_cmap = font.getBestCmap()
    names = {}
    for cp, fallback in ((0x200D, "zwj"), (0xFE0F, "vs16"), (0x1F4AB, "u1F4AB")):
        name = base_cmap.get(cp)
        if name is None:
            name = fallback
            ensure_glyph(font, name, advance=0 if cp in (0x200D, 0xFE0F) else 1000)
            add_cmap(font, cp, name)
        names[cp] = name
    print("component glyphs:", names)

    # visible star for 💫 (placeholder: use the same art scaled down)
    put_bitmap(font, names[0x1F4AB], canvas)
    put_bitmap(font, names[0x200D], None)
    put_bitmap(font, names[0xFE0F], None)

    seq = "miku.seq.spiral"
    ensure_glyph(font, seq, advance=1000)
    put_bitmap(font, seq, canvas)

    rebuild_cblc(font)

    cmap = font.getBestCmap()
    dizzy, star = cmap[0x1F635], cmap[0x1F4AB]
    fea = (f"feature rlig {{\n"
           f"  sub {dizzy} {names[0x200D]} {star} by {seq};\n"
           f"}} rlig;\n")
    open("/tmp/seq.fea", "w").write(fea)
    addOpenTypeFeatures(font, "/tmp/seq.fea")
    font.save(sys.argv[3])
    print("saved", sys.argv[3], len(font.getGlyphOrder()))


if __name__ == "__main__":
    main()
