"""
# Curves

We say that a curve is a function that takes real values and
asigns a value of the codomain to it.

We usually think of it as _time_ hence most of the times the parameter
for the curves will be $t$.
"""

from odeanimate.domains import Interval
from odeanimate.vector import Vector, Vector2D, Vector3D
from odeanimate.codomain import Trajectory
from odeanimate.meta import MathematicalFunction
from odeanimate.utils import (
    cache,
    h as _h,
    RealNumber,
)
from odeanimate.methods.integration import simpson_second_rule


class Curve(MathematicalFunction):
    """Curve Generic Object

    This method implements most of what it's required for curves,
    It will act as a decorator to functions, and the function
    will be gifted with the curve behaviours.

    One of the important assumptions is that functions defined
    in for all of the domain.

    > The function will only get evaluated whenever you request a value.
    > We don't have a way to validate if the evaluation falls out side the domain
    > Like if you are evaluating outside a given interval.


    The Curve Object is capable of doing operations by failling back to the
    codomain features.

        >>> @Curve
        ... def A(t):
        ...     return 1, 2*t
        ...
        >>> @Curve
        ... def B(t):
        ...     return 1, 4*t
        ...

    Peform addition

        >>> (A + B)(0)
        Vector(2, 0)
        >>> (A + Vector(1, 0))(0)
        Vector(2, 0)

    Substraction

        >>> (A - B)(0)
        Vector(0, 0)
        >>> (A - Vector(1, 0))(0)
        Vector(0, 0)

    Multiplication and division

        >>> (A * 2)(0)
        Vector(2, 0)

        >>> (A / 2)(0)
        Vector(0.5, 0.0)

    """

    domain = RealNumber
    codomain = Vector

    def __mul__(self, other):
        """
        Multiplication is allowed by `Curve1D`, `RealNumber` compatible objects
        and by curves of the same kind that could produces a `Curve1D`.

        """

        cls = self.__class__
        if isinstance(other, Curve1D):

            def _new_func(x):
                return self(x) * other(x)

        elif RealNumber.is_compatible(other):

            def _new_func(x):
                return self(x) * other

        elif isinstance(other, self.__class__):

            def _new_func(x):
                return self(x) * other(x)

            cls = Curve1D

        elif isinstance(other, self.codomain):

            def _new_func(x):
                return self(x) * other

            cls = Curve1D

        else:
            raise Exception("Incompatible Mult")
        return cls(function=_new_func)

    def __truediv__(self, other):
        """
        The division will be define as the multiplication against the reciprocal
        of other.

        Examples:

            >>> (Curve1D(lambda x: x**2) / Curve1D(lambda x: -x))(1)
            -1.0
            >>> (Curve1D(lambda x: x**2) / 2)(1)
            0.5
        """
        _new_func = None
        if isinstance(other, Curve1D):

            def _new_func(x):
                return self(x) / other(x)

        elif RealNumber.is_compatible(other):

            def _new_func(x):
                return self(x) / other

        if _new_func is not None:
            return self.__class__(function=_new_func, codomain=self.codomain)
        raise Exception("Can not perform division with non scalar")

    def __abs__(self):
        """
        Examples:
            >>> abs(Curve1D(lambda x: -x))(1)
            1
            >>> abs(Curve2D(lambda x: (x - 3, x - 4)))(0)
            5.0
            >>> abs(Curve3D(lambda x: (x-3, x-4, x)))(0)
            5.0
        """

        def _new_func(x):
            return abs(self(x))

        return Curve1D(function=_new_func)

    def map(self, interval, h=0.1, keys=None):
        if not isinstance(interval, Interval):
            raise Exception("Must evaluate at an interval")
        if h <= 0:
            raise Exception("Delta should be greater than 0.")
        return Trajectory(
            *[(t, *self(t)) for t in interval(h)],
            keys=(keys or self._keys),
        )

    def derivative(self, h=_h):
        def _derivative(t):
            return (self(t + h) - self(t - h)) / (2 * h)

        return self.__class__(codomain=self.codomain, function=_derivative)

    def tangent(self):
        """
        Examples:
            >>> Curve1D(lambda x: x).tangent()(1)
            1.0
            >>> Curve1D(lambda x: x).tangent()(100)
            1.0
            >>> Curve2D(lambda x: (x, 2)).tangent()(100)
            Vector2D(1.0, 0.0)
            >>> Curve3D(lambda x: (x, 2, 0)).tangent()(1)
            Vector3D(1.0, 0.0, 0.0)
        """
        d = self.derivative()
        return d / abs(d)

    def normal(self):
        return self.tangent().tangent()

    def curvature(self):
        return abs(self.tangent().derivative())

    def evolute(self):
        return self + self.normal() / self.curvature()

    def _repr_latex_(self):
        return self.__doc__

    def _plot_2d(self, ax, interval=None, delta=None, **kwargs):
        mpl_kwargs, map_kwargs = {}, {}
        if "color" in kwargs:
            mpl_kwargs["color"] = kwargs["color"]
        if "line" in kwargs:
            mpl_kwargs["marker"] = kwargs["marker"]
        if "keys" in kwargs:
            map_kwargs["keys"] = kwargs["keys"]
        if not isinstance(interval, Interval):
            raise Exception("Missing interval for plot")
        trajectory = self.map(interval, delta, **map_kwargs)
        ax.plot(trajectory.x, trajectory.y, **mpl_kwargs)


class Curve1D(Curve):
    codomain = RealNumber
    _keys = ("x", "y")

    def integrate(self, a, b, h=_h, integrator=simpson_second_rule):
        _integrator = cache(integrator)
        if a <= b:
            interval = Interval(a, b)
            factor = 1
        else:
            interval = Interval(b, a)
            factor = -1
        return factor * sum(
            map(lambda t: _integrator(self, t, t + h), interval(h))
        )

    def __add__(self, other):
        """
        Examples:
            >>> (Curve1D(lambda x: x**2) + Curve1D(lambda x: -x))(1)
            0
            >>> (Curve1D(lambda x: x**2) + 1)(1)
            2
        """
        _new_func = None
        if self.codomain.is_compatible(other):

            def _new_func(x):
                return self(x) + other

        elif isinstance(other, tuple(self.__class__.mro()[:-1])):

            def _new_func(x):
                return self(x) + other(x)

        else:
            raise Exception("Incompatible Sum")
        if _new_func is not None:
            return Curve1D(codomain=self.codomain, function=_new_func)
        return super().__add__(other)

    def __mul__(self, other):
        _new_func = None
        if isinstance(other, Curve1D):

            def _new_func(x):
                return self(x) * other(x)

        elif isinstance(other, self.codomain):

            def _new_func(x):
                return self(x) * other

        if _new_func is not None:
            return Curve1D(codomain=self.codomain, function=_new_func)
        return super().__mul__(other)

    def __rtruediv__(self, other):
        """
        >>> (2 / Curve1D(lambda x: x**2))(1)
        2.0
        """
        _new_func = None
        if RealNumber.is_compatible(other):

            def _new_func(*args, **kwargs):
                return other / self(*args, **kwargs)

        if _new_func is not None:
            return Curve1D(function=_new_func)
        raise TypeError("Can not perform division with non scalar")

    def __pow__(self, other):
        cls, _new_func = Curve1D, None
        if isinstance(other, cls):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) ** other(*args, **kwargs)

        elif RealNumber.is_compatible(other):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) ** other

        else:
            raise Exception(
                f"Incompatible operation between {self.__class__} and {other.__class__}"
            )

        return cls(function=_new_func)

    def map(self, interval, h=0.1, keys=None):
        if not isinstance(interval, Interval):
            raise Exception("Must evaluate at an interval")
        if h <= 0:
            raise Exception("Delta should be greater than 0.")
        return Trajectory(
            *[Vector2D(t, self(t)) for t in interval(h)],
            keys=(keys or self._keys),
        )


class Curve2D(Curve):
    """
    Examples:

        >>> (Curve2D(lambda x: (x**2, x)) + Curve2D(lambda x: (-x, 1)))(0)
        Vector2D(0, 1)
        >>> (Curve2D(lambda x: (x**2, x)) + Vector2D(1, 1))(0)
        Vector2D(1, 1)
        >>> (Curve2D(lambda x: (x**2, x)) * 2)(1)
        Vector2D(2, 2)
        >>> (Curve2D(lambda x: (x**2, x)) * Curve1D(lambda x: x**2))(1)
        Vector2D(1, 1)
        >>> (Curve2D(lambda x: (x**2, x)) * Curve2D(lambda x: (0, 0)))(0)
        0
        >>> (Curve2D(lambda x: (x**2, x)) * Curve2D(lambda x: (1, 1)))(1)
        2
        >>> (Curve2D(lambda x: (x**2, x)) * Vector2D(1, 0))(1)
        1
    """

    codomain = Vector2D
    _keys = ("t", "x", "y")

    @property
    def J(self):
        return Curve2D(function=lambda t: self(t).J)

    def normal(self):
        return self.tangent().J

    def curvature(self):
        d = self.derivative()
        dd = d.derivative()
        return abs(d * dd.J) / (abs(d) ** 3)

    def _plot_2d(self, ax, interval=None, delta=None, **kwargs):
        mpl_kwargs = {}
        if "color" in kwargs:
            mpl_kwargs["color"] = kwargs["color"]
        if "line" in kwargs:
            mpl_kwargs["marker"] = kwargs["marker"]
        if not isinstance(interval, Interval):
            raise Exception("Missing interval for plot")
        trajectory = self.map(interval, delta, keys=["t", "x", "y"])
        ax.plot(trajectory.x, trajectory.y)


class Curve3D(Curve):
    """
    Examples:

        >>> (Curve3D(lambda x: (x**2, x, -x)) + Curve3D(lambda x: (-x, 1, x)))(0)
        Vector3D(0, 1, 0)
        >>> (Curve3D(lambda x: (x**2, x, -x)) + Vector3D(1, 1, 1))(0)
        Vector3D(1, 1, 1)
        >>> (Curve3D(lambda x: (x**2, x, -x)) * 2)(1)
        Vector3D(2, 2, -2)
        >>> (Curve3D(lambda x: (x**2, x, -x)) * Curve1D(lambda x: x**2))(1)
        Vector3D(1, 1, -1)
    """

    codomain = Vector3D
    _keys = ("t", "x", "y", "z")

    def __xor__(self, other):
        _new_func = None
        if isinstance(other, Curve3D):

            def _new_func(t):
                return self(t) ^ other(t)

        elif isinstance(other, Vector3D):

            def _new_func(t):
                return self(t) ^ other

        if _new_func is not None:
            return self.__class__(function=_new_func, codomain=self.codomain)
        raise Exception("Can not do cross product with this function")

    def binormal(self):
        return self.tangent() ^ self.normal()

    def _plot_3d(self, ax, interval=None, delta=None, **kwargs):
        mpl_kwargs = {}
        if "color" in kwargs:
            mpl_kwargs["color"] = kwargs["color"]
        if "line" in kwargs:
            mpl_kwargs["marker"] = kwargs["marker"]
        if not isinstance(interval, Interval):
            raise Exception("Missing interval for plot")
        trajectory = self.map(interval, delta, keys=["t", "x", "y", "z"])
        ax.plot(trajectory.x, trajectory.y, trajectory.z, **mpl_kwargs)
