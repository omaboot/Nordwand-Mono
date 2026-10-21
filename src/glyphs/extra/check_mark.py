from glyphs import Glyph
from draw.stroke_path import draw_stroke_path


class CheckMarkGlyph(Glyph):
    name = "check_mark"
    unicode = "0x2713"
    offset = 0
    width_ratio = 1.15
    stroke_ratio = 1.0

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="cap", width_ratio=self.width_ratio)
        s = self.stroke_ratio * dc.stroke_x
        w = b.x2 - b.x1
        # a short stroke down to the baseline, then the long one up to the cap height
        points = [
            (b.x1 + 0.04 * w, 0.42 * dc.x_height),
            (b.x1 + 0.38 * w, s * 0.55),
            (b.x2 - 0.02 * w, dc.cap - s * 0.3),
        ]
        draw_stroke_path(pen, points, s)
