from numbers import Number
from functools import cache, update_wrapper, wraps
from odeanimate.domains import Interval
from odeanimate.vector import Vector2D, Vector3D
from odeanimate.matrix import Matrix
from odeanimate.utils import h as _h, dense_range, to_list
from odeanimate.methods.integration import simpson_second_rule


class Curve:
    def __init__(self, codomain=None, function=None):
        if codomain is None:
            raise Exception("Codomain is None.")
        if not callable(function):
            raise Exception("Function is not callable")
        self.codomain = codomain
        self._set_function(function)

    def _set_function(self, function):
        self._function = cache(function)
        update_wrapper(self, function)

    def __call__(self, *args, _func=None, **kwargs):
        if callable(args[0]):
            self._set_function(args[0])
            return self
        if self._function is not None:
            _returnable = self._function(*args, **kwargs)
            if isinstance(_returnable, self.codomain):
                return _returnable
            else:
                return self.codomain(*to_list(_returnable))

    def __add__(self, other):
        _new_func = None
        if isinstance(other, self.__class__):

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

    def map(self, interval, h=0.1):
        if not isinstance(interval, Interval):
            raise Exception("Must evaluate at an interval")
        if self.codomain == Number:
            return Matrix(*[(t, self(t)) for t in interval(h)])
        return Matrix(*[(t, *self(t)) for t in interval(h)])

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

        super().__init__(
            codomain=Number, function=_function_wrapper if function else None
        )

    def integrate(self, a, b, h=_h, integrator=simpson_second_rule):
        _integrator = cache(integrator)
        return sum(map(lambda t: _integrator(self, t, t + h), dense_range(a, b, h)))

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
        super().__init__(codomain=Vector2D, function=function)

    @property
    def J(self):
        return Curve2D(function=lambda t: self(t).J)

    def normal(self):
        return self.tangent().J

    def curvature(self):
        d = self.derivative()
        dd = d.derivative()
        return abs(d * dd.J) / abs(d) ** 3


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
        super().__init__(codomain=Vector3D, function=function)

    def __matmul__(self, other):
        _new_func = None
        if isinstance(other, Curve3D):

            def _new_func(t):
                return self(t) @ other(t)

        elif isinstance(other, Vector3D):

            def _new_func(t):
                return self(t) @ other

        if _new_func is not None:
            return self.__class__(function=_new_func, codomain=self.codomain)
        raise Exception("Can not do cross product with this function")

    def binormal(self):
        return self.tangent() @ self.normal()


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
