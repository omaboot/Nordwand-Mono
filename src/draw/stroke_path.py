from math import hypot


def _offset(p, q, t):
    """The segment p→q moved sideways by t (to its left)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = hypot(dx, dy)
    ox, oy = -dy / n * t, dx / n * t
    return (p[0] + ox, p[1] + oy), (q[0] + ox, q[1] + oy)


def _meet(a1, a2, b1, b2):
    """Where the line a1-a2 meets the line b1-b2."""
    d = (a2[0] - a1[0]) * (b2[1] - b1[1]) - (a2[1] - a1[1]) * (b2[0] - b1[0])
    u = ((b1[0] - a1[0]) * (b2[1] - b1[1]) - (b1[1] - a1[1]) * (b2[0] - b1[0])) / d
    return a1[0] + u * (a2[0] - a1[0]), a1[1] + u * (a2[1] - a1[1])


def draw_stroke_path(pen, points, stroke):
    """An open polyline drawn `stroke` wide, mitred at its corners and cut square at its ends."""
    t = stroke / 2
    segs = list(zip(points, points[1:]))
    left = [_offset(p, q, t) for p, q in segs]
    right = [_offset(p, q, -t) for p, q in segs]

    def side(offs):
        pts = [offs[0][0]]
        for (a1, a2), (b1, b2) in zip(offs, offs[1:]):
            pts.append(_meet(a1, a2, b1, b2))
        pts.append(offs[-1][1])
        return pts

    outline = side(right) + side(left)[::-1]
    # counter-clockwise, as the font's other outlines
    area = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(outline, outline[1:] + outline[:1]))
    if area < 0:
        outline.reverse()
    pen.moveTo(outline[0])
    for pt in outline[1:]:
        pen.lineTo(pt)
    pen.closePath()
