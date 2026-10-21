from glyphs import Glyph
from draw.circle import draw_circle
from draw.rect import draw_rect


class PlaceOfInterestSignGlyph(Glyph):
    """⌘: a square whose four sides run on into a loop at each corner."""

    name = "place_of_interest_sign"
    unicode = "0x2318"
    offset = 0
    half_extent = 0.42  # of the cell's width, to the loops' outer edge
    side_to_loop = 1.15  # the square's half side, in loop radii

    def draw(self, pen, dc):
        t = 0.6 * dc.stroke_x + 15  # lighter than the letters, so the loops stay open in bold
        cx, cy = dc.window_width / 2 + self.offset, dc.cap / 2
        e = self.half_extent * dc.window_width
        r = (e - t / 2) / (self.side_to_loop + 2)
        half = self.side_to_loop * r
        reach = half + r
        for sx in (-1, 1):
            draw_rect(pen, cx + sx * half - t / 2, cy - reach, cx + sx * half + t / 2, cy + reach)
        for sy in (-1, 1):
            draw_rect(pen, cx - reach, cy + sy * half - t / 2, cx + reach, cy + sy * half + t / 2)
        for sx in (-1, 1):
            for sy in (-1, 1):
                lx, ly = cx + sx * reach, cy + sy * reach
                draw_circle(pen, lx, ly, r + t / 2, clockwise=False)
                draw_circle(pen, lx, ly, r - t / 2, clockwise=True)
