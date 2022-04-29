from math import sin, cos, pi
from numbers import Number
from odeanimate.vector import Vector2D
from odeanimate.curve import Curve, Curve2D


def circle(*p, center=None, r=None):
    """Circle generator function
    This works with
    - center and radius
    - 3 points, no circle and no radius
    - 2 points and center
    - 2 points, and radius

    It returns a Curve2D, with domain (0, 1), as a
    circle's parametric curve.
    """
    if isinstance(center, Vector2D) and isinstance(r, Number) and r > 0:
        h, k = center.x, center.y
    else:
        raise Exception

    @Curve2D
    def _circle(t):
        return r * cos(2 * pi * t) + h, r * sin(2 * pi * t) + k

    return _circle


def line(p, q, m=None):
    def _line(t):
        return t * (q - p) + p

    return Curve(codomain=p.__class__, function=_line)
