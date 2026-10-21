#!/usr/bin/env python3
"""Cut the Regular and Bold TTFs down to a small web font: Basic Latin, what the font has of
Latin-1, and the punctuation, arrows and symbols listed below, without ligatures or alternates. Writes a WOFF2
per weight and the list of characters they cover, for a site's build to check its pages against.

Usage: python -m scripts.web_cut [--out DIR]   (after `make build-ttf`)
"""

import argparse
import os

from fontTools import subset
from fontTools.ttLib import TTFont

# Beyond Basic Latin and Latin-1: dashes, quotes, the ellipsis, angle quotes, arrows, ⌘ and ✓.
EXTRA = [0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2026, 0x2039, 0x203A,
         0x2190, 0x2191, 0x2192, 0x2193, 0x2197, 0x2318, 0x2713]
UNICODES = list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + EXTRA
WEIGHTS = {"Regular": 400, "Bold": 700}


def cut(src, dst):
    o = subset.Options()
    o.layout_features = []  # no ligatures (-> stays two characters in prose), no alternates
    o.hinting = False
    o.desubroutinize = True
    # the names and the copyright, not the license text (ID 13, several KB): ship LICENSE-FONT.txt
    # beside the fonts instead, as the OFL asks
    o.name_IDs = [0, 1, 2, 3, 4, 5, 6, 14]
    font = TTFont(src)
    s = subset.Subsetter(o)
    s.populate(unicodes=UNICODES)
    s.subset(font)
    font.flavor = "woff2"
    font.save(dst)
    return set(font.getBestCmap())


def ranges(cps):
    out, start, prev = [], None, None
    for cp in sorted(cps):
        if start is None:
            start = prev = cp
        elif cp == prev + 1:
            prev = cp
        else:
            out.append((start, prev))
            start = prev = cp
    out.append((start, prev))
    return [f"{a:04X}" if a == b else f"{a:04X}-{b:04X}" for a, b in out]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--src", default="fonts/ttf")
    ap.add_argument("--out", default="fonts/web-cut")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    covered = None
    for style, weight in WEIGHTS.items():
        dst = os.path.join(a.out, f"NordwandMono-{weight}.woff2")
        cps = cut(os.path.join(a.src, f"NordwandMono-{style}.ttf"), dst)
        missing = set(UNICODES) - cps
        if missing & (set(range(0x20, 0x7F)) | set(EXTRA)):
            raise SystemExit(f"{style}: no glyph for {', '.join(f'U+{c:04X}' for c in sorted(missing))}")
        if missing:
            print(f"{style}: Latin-1 left out (no glyph yet): {' '.join(chr(c) for c in sorted(missing))}")
        covered = cps if covered is None else covered & cps
        print(f"{dst}: {os.path.getsize(dst)} bytes, {len(cps)} characters")
    with open(os.path.join(a.out, "NordwandMono-chars.txt"), "w") as f:
        f.write("# The characters both weights of this web cut cover, as code point ranges.\n")
        f.write("\n".join(ranges(covered)) + "\n")


if __name__ == "__main__":
    main()
