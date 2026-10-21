from fontTools.misc.transform import Transform
from fontTools.pens.transformPen import TransformPen


def draw_transformed(pen, glyph, dc, transform):
    """Draw another glyph through an affine transform (a rotation, a mirror, a shift)."""
    glyph.draw(TransformPen(pen, transform), dc)


def about(cx, cy, transform):
    """`transform` applied around the point (cx, cy) instead of the origin."""
    return Transform().translate(cx, cy).transform(transform).translate(-cx, -cy)
