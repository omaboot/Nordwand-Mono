from glyphs import Glyph
from draw.chevron import draw_chevron


class _AngleQuotationMark(Glyph):
    """‹ and ›: the < > chevron, smaller and centred on the x-height."""

    offset = 0
    width_ratio = 1
    half_width = 0.3
    span = 0.4
    stroke_ratio = 1.25
    points_right = True

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="x_height", width_ratio=self.width_ratio)
        s = dc.stroke_x * self.stroke_ratio
        w = self.half_width * b.width
        tip, back = (b.xmid + w, b.xmid - w) if self.points_right else (b.xmid - w, b.xmid + w)
        draw_chevron(pen, s, s, tip, back, b.height / 2, dc.parenthesis_length * self.span, delta=s)


class SingleLeftPointingAngleQuotationMarkGlyph(_AngleQuotationMark):
    name = "single_left_pointing_angle_quotation_mark"
    unicode = "0x2039"
    points_right = False


class SingleRightPointingAngleQuotationMarkGlyph(_AngleQuotationMark):
    name = "single_right_pointing_angle_quotation_mark"
    unicode = "0x203A"


class _DoubleAngleQuotationMark(_AngleQuotationMark):
    """« and »: two of the single marks, side by side."""

    half_width = 0.2
    gap = 0.36  # between the two marks' middles, of the body's width

    def draw(self, pen, dc):
        from fontTools.misc.transform import Transform
        from fontTools.pens.transformPen import TransformPen

        b = dc.body_bounds(offset=self.offset, height="x_height", width_ratio=self.width_ratio)
        d = self.gap * b.width / 2
        for dx in (-d, d):
            _AngleQuotationMark.draw(self, TransformPen(pen, Transform().translate(dx, 0)), dc)


class LeftPointingDoubleAngleQuotationMarkGlyph(_DoubleAngleQuotationMark):
    name = "left_pointing_double_angle_quotation_mark"
    unicode = "0xAB"
    points_right = False


class RightPointingDoubleAngleQuotationMarkGlyph(_DoubleAngleQuotationMark):
    name = "right_pointing_double_angle_quotation_mark"
    unicode = "0xBB"
