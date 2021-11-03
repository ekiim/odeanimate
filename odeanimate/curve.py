from functools import cache
from odeanimate.vector import Vector2D, Vector3D
from odeanimate.utils import h as _h, dense_range
from odeanimate.methods.integration import simpson_second_rule


class Curve:
    def __init__(self, codomain=None, function=None):
        if codomain is None:
            raise Exception("Codomain is None.")
        if not callable(function):
            raise Exception("Function is not callable")
        self.codomain = codomain
        self.set_function(function)

    def set_function(self, function):
        self._function = cache(function)

    def __call__(self, *args, _func=None, **kwargs):
        if callable(args[0]):
            self.set_function(args[0])
            return self
        if self._function is not None:
            return self.codomain(*self._function(*args, **kwargs))

    def derivative(self, h=_h):
        def _derivative(t):
            return (self(t + h) - self(t - h)) / (2*h)
        return self.__class__(codomain=self.codomain, function=_derivative)


class Curve1D(Curve):
    def __init__(self, function=None, **kwargs):

        def _function_wrapper(*args, **kwargs):
            return (function(*args, **kwargs),)

        super().__init__(
            codomain=float,
            function=_function_wrapper if function else None
        )

    def integrate(self, a, b, h=_h, integrator=simpson_second_rule):
        _integrator = cache(integrator)
        return sum(map(
            lambda t: _integrator(self, t, t+h),
            dense_range(a, b, h)
        ))


class Curve2D(Curve):
    def __init__(self, function=None, **kwargs):
        super().__init__(codomain=Vector2D, function=function)


class Curve3D(Curve):
    def __init__(self, function=None, **kwargs):
        super().__init__(codomain=Vector3D, function=function)
