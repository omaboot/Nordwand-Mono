from glyphs import Glyph
from glyphs.special.full_stop import FullStopGlyph
from draw.rect import draw_rect


class MiddleDotGlyph(Glyph):
    name = "middle_dot"
    unicode = "0xB7"
    offset = 0
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        # the full stop's square, centred on the x-height's middle
        s = FullStopGlyph.stroke_ratio * dc.stroke_x
        y = b.height / 2
        draw_rect(pen, b.xmid - s / 2, y - s / 2, b.xmid + s / 2, y + s / 2)
