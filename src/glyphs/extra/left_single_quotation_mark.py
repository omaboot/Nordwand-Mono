from math import pi

from fontTools.misc.transform import Transform

from glyphs import Glyph
from glyphs.special.right_single_quotation_mark import RightSingleQuotationMarkGlyph
from draw.transformed import about, draw_transformed


def quote_centre(dc, quote):
    """The middle of the ’ mark's outline, which a ‘ turns around."""
    b = dc.body_bounds(offset=quote.offset, height="x_height", width_ratio=quote.width_ratio)
    h = quote.height_ratio * b.height
    return b.xmid - quote.delta * b.width / 2, dc.ascent - h / 2


class LeftSingleQuotationMarkGlyph(Glyph):
    name = "left_single_quotation_mark"
    unicode = "0x2018"
    offset = 0

    def draw(self, pen, dc):
        quote = RightSingleQuotationMarkGlyph()
        cx, cy = quote_centre(dc, quote)
        draw_transformed(pen, quote, dc, about(cx, cy, Transform().rotate(pi)))
