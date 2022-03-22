from numbers import Number
from functools import cache, update_wrapper, wraps
from odeanimate.vector import Vector2D, Vector3D
from odeanimate.utils import h as _h, dense_range, to_list
from odeanimate.methods.integration import simpson_second_rule


class Curve:
    def __init__(self, codomain=None, function=None):
        if codomain is None:
            raise Exception("Codomain is None.")
        if not callable(function):
            raise Exception("Function is not callable")
        self.codomain = codomain
        self.set_function(function)
        self._codomain_class = codomain

    def set_function(self, function):
        self._function = cache(function)
        update_wrapper(self, function)

    def __call__(self, *args, _func=None, **kwargs):
        if callable(args[0]):
            self.set_function(args[0])
            return self
        if self._function is not None:
            _returnable = self._function(*args, **kwargs)
            if isinstance(_returnable, self.codomain):
                return _returnable
            else:
                return self._codomain_class(*to_list(_returnable))

    def derivative(self, h=_h):
        def _derivative(t):
            return (self(t + h) - self(t - h)) / (2 * h)

        return self.__class__(codomain=self.codomain, function=_derivative)

    def __add__(self, other):
        _new_func = None
        if isinstance(other, Curve) and self.codomain == other.codomain:

            def _new_func(x):
                return self(x) + other(x)

        else:
            raise Exception("Incompatible Sum")
        if _new_func is not None:
            return self.__class__(codomain=self.codomain, function=_new_func)
        raise Exception("Can not resolve function")


class Curve1D(Curve):
    def __init__(self, function=None, **kwargs):
        @wraps(function)
        def _function_wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        super().__init__(
            codomain=Number, function=_function_wrapper if function else None
        )
        # self._codomain_class = float

    def integrate(self, a, b, h=_h, integrator=simpson_second_rule):
        _integrator = cache(integrator)
        return sum(map(lambda t: _integrator(self, t, t + h), dense_range(a, b, h)))

    def __add__(self, other):
        """
        >>> (Curve1D(lambda x: x**2) + Curve1D(lambda x: -x))(1)
        0
        >>> (Curve1D(lambda x: x**2) + 1)(1)
        2
        """
        _new_func = None
        if isinstance(other, Curve1D):

            def _new_func(x):
                return self(x) + other(x)

        elif isinstance(other, Number):

            def _new_func(x):
                return self(x) + other

        else:
            return super().__add__(other)
        if _new_func is not None:
            return Curve1D(_new_func)
        raise Exception("Can not resolve function")

    def __mul__(self, other):
        if isinstance(other, Curve1D):

            def _new_func(x):
                return self(x) * other(x)

        elif isinstance(other, Number):

            def _new_func(x):
                return self(x) * other

        else:
            raise Exception("Incompatible Mult")
        return Curve1D(function=_new_func)


class Curve2D(Curve):
    def __init__(self, function=None, **kwargs):
        super().__init__(codomain=Vector2D, function=function)

    def __add__(self, other):
        _new_func = None
        if isinstance(other, Curve1D):

            def _new_func(x):
                return self(x) + other(x)

        elif isinstance(other, Number):

            def _new_func(x):
                return self(x) + other

        else:
            raise Exception("Incompatible Sum")
        if _new_func is not None:
            return Curve1D(_new_func)
        raise Exception("Can not resolve function")


class Curve3D(Curve):
    def __init__(self, function=None, **kwargs):
        super().__init__(codomain=Vector3D, function=function)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
