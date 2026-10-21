from math import pi

from fontTools.misc.transform import Transform

from glyphs import Glyph
from glyphs.special.quotation_mark import QuotationMarkGlyph
from glyphs.special.right_single_quotation_mark import RightSingleQuotationMarkGlyph
from glyphs.extra.left_single_quotation_mark import quote_centre
from draw.transformed import about, draw_transformed


def draw_pair(pen, dc, turned):
    """Two ’ marks (or two ‘ when turned) spaced as the straight " is."""
    quote = RightSingleQuotationMarkGlyph()
    b = dc.body_bounds(offset=0, height="x_height", width_ratio=QuotationMarkGlyph.width_ratio)
    half = QuotationMarkGlyph.gap * b.width / 2 + dc.stroke_x / 2
    cx, cy = quote_centre(dc, quote)
    turn = about(cx, cy, Transform().rotate(pi)) if turned else Transform()
    for dx in (-half, half):
        draw_transformed(pen, quote, dc, Transform().translate(dx, 0).transform(turn))


class LeftDoubleQuotationMarkGlyph(Glyph):
    name = "left_double_quotation_mark"
    unicode = "0x201C"
    offset = 0

    def draw(self, pen, dc):
        draw_pair(pen, dc, turned=True)


class RightDoubleQuotationMarkGlyph(Glyph):
    name = "right_double_quotation_mark"
    unicode = "0x201D"
    offset = 0

    def draw(self, pen, dc):
        draw_pair(pen, dc, turned=False)
