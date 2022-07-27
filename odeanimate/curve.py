from numbers import Number
from functools import lru_cache, update_wrapper, wraps
from odeanimate.domains import Interval
from odeanimate.vector import Vector2D, Vector3D
from odeanimate.codomain import Trajectory
from odeanimate.utils import h as _h, to_list
from odeanimate.methods.integration import simpson_second_rule


cache = lru_cache(maxsize=None)


class Curve:
    def __init__(self, codomain=None, function=None, keys=None):
        if codomain is None:
            raise Exception("Codomain is None.")
        if not callable(function):
            raise Exception("Function is not callable")
        self.codomain = codomain
        self._set_function(function)
        self._keys = keys

    def _set_function(self, function):
        self._function = cache(function)
        update_wrapper(self, function)

    def __call__(self, *args, _func=None, **kwargs):
        if callable(args[0]):
            self._set_function(args[0])
            return self
        if self._function is not None:
            _returnable = self._function(*args, **kwargs)
            if isinstance(_returnable, self.codomain) or self.codomain is Number:
                return _returnable
            else:
                return self.codomain(*to_list(_returnable))

    def __add__(self, other):
        _new_func = None
        if isinstance(other, tuple(self.__class__.mro())[:-1]):

            def _new_func(x):
                return self(x) + other(x)

        elif isinstance(other, Curve) and self.codomain == other.codomain:

            def _new_func(x):
                return self(x) + other(x)

        elif isinstance(other, self.codomain):

            def _new_func(x):
                return self(x) + other

        else:
            raise Exception("Incompatible Sum")
        if _new_func is not None:
            return self.__class__(codomain=self.codomain, function=_new_func)
        raise Exception("Can not resolve function")

    def __sub__(self, other):
        return self + (-1) * other

    def __mul__(self, other):
        cls = self.__class__
        if isinstance(other, Curve1D):

            def _new_func(x):
                return self(x) * other(x)

        elif isinstance(other, Number):

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
        >>> (Curve1D(lambda x: x**2) / Curve1D(lambda x: -x))(1)
        -1.0
        >>> (Curve1D(lambda x: x**2) / 2)(1)
        0.5
        """
        _new_func = None
        if isinstance(other, Curve1D):

            def _new_func(x):
                return self(x) / other(x)

        elif isinstance(other, Number):

            def _new_func(x):
                return self(x) / other

        if _new_func is not None:
            return self.__class__(function=_new_func, codomain=self.codomain)
        raise Exception("Can not perform division with non scalar")

    def __abs__(self):
        """
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
        if self.codomain == Number:
            return Trajectory(
                *[(t, self(t)) for t in interval(h)], keys=(keys or self._keys)
            )
        return Trajectory(
            *[(t, *self(t)) for t in interval(h)], keys=(keys or self._keys)
        )

    def derivative(self, h=_h):
        def _derivative(t):
            return (self(t + h) - self(t - h)) / (2 * h)

        return self.__class__(codomain=self.codomain, function=_derivative)

    def tangent(self):
        """
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
        if not isinstance(interval, Interval):
            raise Exception("Missing interval for plot")
        trayectory = self.map(interval, delta)
        ax.plot(trayectory.x, trayectory.y)


class Curve1D(Curve):
    """
    >>> (Curve1D(lambda x: x**2) + Curve1D(lambda x: -x))(1)
    0
    >>> (Curve1D(lambda x: x**2) + 1)(1)
    2
    """

    def __init__(self, function=None, **kwargs):
        @wraps(function)
        def _function_wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        if kwargs.get("keys", None) is None:
            kwargs["keys"] = ("x", "y")

        kwargs["codomain"] = Number
        super().__init__(function=_function_wrapper if function else None, **kwargs)

    def integrate(self, a, b, h=_h, integrator=simpson_second_rule):
        _integrator = cache(integrator)
        if a <= b:
            interval = Interval(a, b)
            factor = 1
        else:
            interval = Interval(b, a)
            factor = -1
        return factor * sum(map(lambda t: _integrator(self, t, t + h), interval(h)))

    def __add__(self, other):
        _new_func = None
        if isinstance(other, self.codomain):

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
        if isinstance(other, Number):

            def _new_func(x):
                return other / self(x)

        if _new_func is not None:
            return Curve1D(function=_new_func)
        raise TypeError("Can not perform division with non scalar")

    def __pow__(self, other):
        return Curve1D(function=lambda t: self(t) ** other)

    def _plot_2d(self, ax, interval=None, delta=None, **kwargs):
        if not isinstance(interval, Interval):
            raise Exception("Missing interval for plot")
        trayectory = self.map(interval, delta, keys=["x", "y"])
        ax.plot(trayectory.x, trayectory.y)


class Curve2D(Curve):
    """
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

    def __init__(self, function=None, **kwargs):
        kwargs["codomain"] = Vector2D
        if kwargs.get("keys", None) is None:
            kwargs["keys"] = ("t", "x", "y")
        super().__init__(function=function, **kwargs)

    @property
    def J(self):
        return Curve2D(function=lambda t: self(t).J)

    def normal(self):
        return self.tangent().J

    def curvature(self):
        d = self.derivative()
        dd = d.derivative()
        return abs(d * dd.J) / abs(d) ** 3

    def _plot_2d(self, ax, interval=None, delta=None, **kwargs):
        if not isinstance(interval, Interval):
            raise Exception("Missing interval for plot")
        trayectory = self.map(interval, delta, keys=["t", "x", "y"])
        ax.plot(trayectory.x, trayectory.y)


class Curve3D(Curve):
    """
    >>> (Curve3D(lambda x: (x**2, x, -x)) + Curve3D(lambda x: (-x, 1, x)))(0)
    Vector3D(0, 1, 0)
    >>> (Curve3D(lambda x: (x**2, x, -x)) + Vector3D(1, 1, 1))(0)
    Vector3D(1, 1, 1)
    >>> (Curve3D(lambda x: (x**2, x, -x)) * 2)(1)
    Vector3D(2, 2, -2)
    >>> (Curve3D(lambda x: (x**2, x, -x)) * Curve1D(lambda x: x**2))(1)
    Vector3D(1, 1, -1)
    """

    def __init__(self, function=None, **kwargs):
        kwargs["codomain"] = Vector3D
        if kwargs.get("keys", None) is None:
            kwargs["keys"] = ("t", "x", "y", "z")
        super().__init__(function=function, **kwargs)

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
        if not isinstance(interval, Interval):
            raise Exception("Missing interval for plot")
        trayectory = self.map(interval, delta, keys=["t", "x", "y", "z"])
        ax.plot(trayectory.x, trayectory.y, trayectory.z)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
