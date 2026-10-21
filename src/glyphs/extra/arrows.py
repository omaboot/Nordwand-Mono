from math import pi

from fontTools.misc.transform import Transform

from glyphs import Glyph
from glyphs.special.right_arrow import RightArrowGlyph
from draw.transformed import about, draw_transformed


class _TurnedArrow(Glyph):
    """The → turned or mirrored: ← on the same axis, the others about the cap's middle."""

    offset = 0
    angle = 0.0
    mirror = False
    scale = 1.0
    stretch = (1.0, 1.0)  # after turning: across, along the page

    def draw(self, pen, dc):
        arrow = RightArrowGlyph()
        if self.mirror:
            draw_transformed(pen, arrow, dc, about(dc.window_width / 2, dc.math, Transform().scale(-1, 1)))
            return
        # move the arrow's middle from the math axis to the cap's middle, then turn it there
        cx, cy = dc.window_width / 2, dc.cap / 2
        t = about(cx, cy, Transform().scale(*self.stretch).rotate(self.angle).scale(self.scale)).translate(0, cy - dc.math)
        draw_transformed(pen, arrow, dc, t)


class LeftArrowGlyph(_TurnedArrow):
    name = "left_arrow"
    unicode = "0x2190"
    mirror = True


class UpArrowGlyph(_TurnedArrow):
    name = "up_arrow"
    unicode = "0x2191"
    angle = pi / 2
    # its head is as wide as the → is tall: narrower to stay inside the cell, longer to reach
    # from the baseline to the cap height
    stretch = (0.86, 1.1)


class DownArrowGlyph(_TurnedArrow):
    name = "down_arrow"
    unicode = "0x2193"
    angle = -pi / 2
    stretch = (0.86, 1.1)


class NorthEastArrowGlyph(_TurnedArrow):
    name = "north_east_arrow"
    unicode = "0x2197"
    angle = pi / 4
    scale = 0.85
