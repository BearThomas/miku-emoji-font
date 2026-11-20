#!/usr/bin/env python3
"""Build a dual-art CBDT emoji font: small strikes = high-visibility art,
large strikes = faithful (official-reference) art.

The CBDT/CBLC format stores a separate image set per ppem strike, so the same
codepoint can look different at 20px and 64px. That lets us keep the bold,
readable version in the emoji picker and the faithful version in large text.
"""
import os, io, json, argparse
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.C_B_D_T_ import SmallGlyphMetrics, cbdt_bitmap_format_17
from fontTools.ttLib.tables.E_B_L_C_ import eblc_index_sub_table_1
from fontTools.feaLib.builder import addOpenTypeFeatures

BLANK = None
SMALL_MAX_PPEM = 32


def blank_png():
    global BLANK
    if BLANK is None:
        buf = io.BytesIO()
        Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(buf, format="PNG")
        BLANK = buf.getvalue()
    return BLANK


def normalize(path, size=1024, pad=0.02):
    im = Image.open(path).convert("RGBA")
    bb = im.getbbox()
    if bb:
        im = im.crop(bb)
    art = int(size * (1 - 2 * pad))
    im = im.resize((art, art), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    off = (size - art) // 2
    canvas.paste(im, (off, off), im)
    return canvas


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


def put_bitmap(font, gname, im, idx, bearing=0.85):
    cbdt = font["CBDT"]
    bst = font["CBLC"].strikes[idx].bitmapSizeTable
    px, py = bst.ppemX, bst.ppemY
    if im is None:
        data, w, h = blank_png(), 1, 1
    else:
        buf = io.BytesIO()
        im.resize((px, py), Image.LANCZOS).save(buf, format="PNG", optimize=True)
        data, w, h = buf.getvalue(), px, py
    m = SmallGlyphMetrics()
    m.height, m.width = h, w
    m.BearingX = 0
    m.BearingY = min(round(h * bearing), 127)
    m.Advance = 0 if im is None else px
    g = cbdt_bitmap_format_17(b"", font)
    g.imageData = data
    g.metrics = m
    cbdt.strikeData[idx][gname] = g


def rebuild_cblc(font):
    cbdt, cblc = font["CBDT"], font["CBLC"]
    order = font.getGlyphOrder()
    idx = {g: i for i, g in enumerate(order)}
    for i, strike in enumerate(cblc.strikes):
        names = [g for g in order[1:] if g in cbdt.strikeData[i]]
        names.sort(key=lambda g: idx[g])
        ist = eblc_index_sub_table_1(b"", font)
        ist.indexFormat = 1
        ist.imageFormat = 17
        ist.imageDataOffset = 0
        ist.firstGlyphIndex = idx[names[0]]
        ist.lastGlyphIndex = idx[names[-1]]
        ist.names = names
        strike.indexSubTables = [ist]
        bst = strike.bitmapSizeTable
        bst.startGlyphIndex, bst.endGlyphIndex = idx[names[0]], idx[names[-1]]
        bst.numberOfIndexSubTables = 1


def load_art(directory, manifest, cmap, pad):
    out = {}
    for fname, cp in manifest.items():
        cp = int(cp[2:], 16) if isinstance(cp, str) else int(cp)
        gname = cmap.get(cp)
        path = os.path.join(directory, fname)
        if gname and os.path.exists(path):
            out[gname] = normalize(path, pad=pad)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--art", required=True, help="high-visibility art (small strikes)")
    ap.add_argument("--art-large", default=None, help="faithful art (large strikes)")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--sequences", default=None)
    ap.add_argument("--subset", required=True)
    ap.add_argument("--family", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pad", type=float, default=0.02)
    ap.add_argument("--scale", type=float, default=1.1)
    ap.add_argument("--bearing", type=float, default=0.85)
    args = ap.parse_args()

    manifest = json.load(open(args.manifest))
    sequences = json.load(open(args.sequences)) if args.sequences else {}
    font = TTFont(args.subset)
    cmap = font.getBestCmap()

    for nid, val in ((1, args.family), (2, "Regular"), (3, f"{args.family} 1.0"),
                     (4, f"{args.family} Regular"), (6, args.family.replace(" ", "") + "-Regular")):
        font["name"].setName(val, nid, 3, 1, 0x409)
        font["name"].setName(val, nid, 1, 0, 0)

    small = load_art(args.art, manifest, cmap, args.pad)
    large = load_art(args.art_large, manifest, cmap, args.pad) if args.art_large else {}

    # invisible joiners
    for cp in (0x200D, 0xFE0F):
        gname = cmap.get(cp)
        if gname is None:
            gname = f"uni{cp:04X}"
            ensure_glyph(font, gname, advance=0)
            add_cmap(font, cp, gname)

    rules = []
    seq_small, seq_large = {}, {}
    for fname, seq in sequences.items():
        cps = [int(x, 16) for x in seq.split()]
        gname = "miku.seq." + "_".join(f"{c:04X}" for c in cps)
        ensure_glyph(font, gname)
        for attr, src in ((seq_small, args.art), (seq_large, args.art_large)):
            path = os.path.join(src, fname) if src else None
            if path and os.path.exists(path):
                attr[gname] = normalize(path, pad=args.pad)
        if gname not in seq_small and gname not in seq_large:
            continue
        parts = [cmap[c] for c in cps if c != 0xFE0F and cmap.get(c)]
        rules.append(f"  sub {' '.join(parts)} by {gname};")
        nz = [p for p in parts if p != cmap.get(0x200D)]
        if nz != parts:
            rules.append(f"  sub {' '.join(nz)} by {gname};")

    for i, strike in enumerate(font["CBLC"].strikes):
        ppem = strike.bitmapSizeTable.ppemY
        use_large = ppem > SMALL_MAX_PPEM
        for gname, im in small.items():
            chosen = (large.get(gname) if use_large else None) or im
            put_bitmap(font, gname, chosen, i, bearing=args.bearing)
        for gname in set(seq_small) | set(seq_large):
            chosen = (seq_large.get(gname) if use_large else None) or seq_small.get(gname)
            if chosen is not None:
                put_bitmap(font, gname, chosen, i, bearing=args.bearing)
        for cp in (0x200D, 0xFE0F):
            gname = cmap.get(cp)
            if gname:
                put_bitmap(font, gname, None, i)

    rebuild_cblc(font)

    if rules:
        open("/tmp/miku_seq.fea", "w").write("feature rlig {\n" + "\n".join(rules) + "\n} rlig;\n")
        addOpenTypeFeatures(font, "/tmp/miku_seq.fea")

    font.save(args.out)
    n_large = sum(1 for g in large if g in small)
    print(f"wrote {args.out} ({os.path.getsize(args.out)} bytes), "
          f"glyphs={len(font.getGlyphOrder())}, faithful art for {n_large} codepoints")


if __name__ == "__main__":
    main()
