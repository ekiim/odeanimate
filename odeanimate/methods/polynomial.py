from numbers import Number
from odeanimate.utils import nth_roots_of_unity
from odeanimate.curve import Curve1D


class Polynomial(Curve1D):
    def __init__(self, *coefs, **kwargs):
        self.coefs = tuple(coefs)

        def _evaluation_function(x):
            return sum((a * (x**i) for i, a in enumerate(self.coefs)))

        super().__init__(function=_evaluation_function)

    @property
    def degree(self):
        return len(self.coefs) - 1

    def __add__(self, other):
        new_coefs = None
        if isinstance(other, Polynomial):
            bigger = max((self, other), key=lambda i: i.degree)
            smaller = min((self, other), key=lambda i: i.degree)
            new_coefs = [a + b for a, b in zip(self.coefs, other.coefs)]
            new_coefs.extend(bigger.coefs[1 + smaller.degree :])
        if isinstance(other, Number):
            new_coefs = (self.coefs[0] + other, *self.coefs[1:])
        if new_coefs:
            return Polynomial(*new_coefs)
        return super(Polynomial, self).__add__(other)

    def __mul__(self, other):
        new_coefs = None
        if isinstance(other, Number):
            new_coefs = [other * c for c in self.coefs]
        if new_coefs:
            return Polynomial(*new_coefs)
        return super(Polynomial, self).__mul__(other)

    def __repr__(self):
        return f"<Polynomial {self.coefs}>"

    def complex_evaluation(self, z):
        return self._function(z)[0]

    def point_value(self, x):
        return x, self.complex_evaluation(x)

    def point_values(self, *xs):
        return [self.point_value(x) for x in xs]
