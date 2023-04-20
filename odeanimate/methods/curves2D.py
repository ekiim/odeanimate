"""
Two Dimensional Typical Parametric Curves

This can work as an example of 2D paramteric curves.

This functions are taken from [@GrayModernDiffGeo].
(Check bibliography)

TODO:
    - Add Docstrings to explain the actual curves.
    - Implement Curves that require an Integral to
    be computed.
    - Define each curve as a SubClass of Curve2D,
    in order to implement their exact derivative and
    curvatures.

"""

from math import cos, e, pi, sin, cosh, log, tan
from odeanimate.vector import Vector2D
from odeanimate.curve import Curve2D


def Ellipses(a=2, b=1, c=Vector2D(0, 0)):
    @Curve2D
    def _ellipses(t):
        return (
            a * cos(2 * pi * t) + c.x,
            b * sin(2 * pi * t) + c.y,
        )

    return _ellipses


def Circle(r=1, c=Vector2D(0, 0)):
    return Ellipses(r, r, c)


def LogarithmicSpirals(a, b):
    @Curve2D
    def _log_spiral(t):
        return (
            a * e ** (b * t) * cos(2 * pi * t),
            a * e ** (b * t) * sin(2 * pi * t),
        )


def SemicubicalParabola(t):
    return t**2, t**3


"""
Exercises from section 1.8 from [@GrayModernDiffGeo]
"""


def _gray_exercises_sec_1_8_no_1_a(a=1):
    @Curve2D
    def returnable(t):
        return (a * (cos(t) + t * sin(t)), a * (sin(t) - t * cos(t)))

    return returnable


def _gray_exercises_sec_1_8_no_1_b(a=1):
    @Curve2D
    def returnable(t):
        return (a * (cosh(t / a)), t)

    return returnable


def _gray_exercises_sec_1_8_no_1_c(a=1):
    @Curve2D
    def returnable(t):
        return (a * cos(t) ** 3, sin(t) ** 3)

    return returnable


def _gray_exercises_sec_1_8_no_1_d(a=1):
    @Curve2D
    def returnable(t):
        return (a * 2 * t, t**2)

    return returnable


def _gray_exercises_sec_1_8_no_8(a=1):
    @Curve2D
    def returnable(t):
        try:
            return (t, (abs(t) ** a) * sin(1 / t))
        except ZeroDivisionError:
            return 0, 0

    return returnable


def Cycloid(a=1, b=0.5):
    @Curve2D
    def returnable(t):
        return (
            a * t - b * sin(t),
            a - b * cos(t),
        )

    return returnable


def Lemniscate(a):
    @Curve2D
    def returnable(t):
        r = 1 + sin(t) ** 2
        return (a / r * cos(t), a / r * sin(t) * cos(t))

    return returnable


def Cardioid(a):
    @Curve2D
    def returnable(t):
        r = 2 * a * (1 + cos(t))
        return (r * cos(t), r * sin(t))

    return returnable


def Catenary(a):
    @Curve2D
    def returnable(t):
        return (a * cosh(t / a), t)

    return returnable


def Cissoid(a):
    @Curve2D
    def returnable(t):
        r = 2 * a * (t**2) / (1 + t**2)
        return (r, r * t)

    return returnable


def Tractrix(a):
    @Curve2D
    def returnable(t):
        return (a * sin(t), cos(t) + log(tan(t / 2)))

    return returnable


def Clothiods(a):
    raise NotImplemented
