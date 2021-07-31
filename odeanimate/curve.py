from odeanimate.vector import Vector2D


class Curve:
    def __init__(self, codomain=None, callable=None):
        if codomain is None:
            raise Exception("Codomain is None.")
        self.codomain = codomain
        self._callable = callable

    def __call__(self, *args, _func=None, **kwargs):
        if callable(args[0]):
            self._callable = args[0]
            return self
        if self._callable is not None:
            return self.codomain(*self._callable(*args, **kwargs))

    def derivative(self, h=0.001):
        def _derivative(t):
            return (self(t + h) - self(t - h)) / (2*h)
        return self.__class__(codomain=self.codomain, callable=_derivative)


class Curve2D(Curve):
    def __init__(self, callable=None, **kwargs):
        self.codomain = Vector2D
        self._callable = callable
