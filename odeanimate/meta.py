"""
Mixins
"""
from functools import lru_cache, update_wrapper, wraps
from odeanimate.utils import RealNumber

cache = lru_cache(maxsize=None)


class MathematicalFunction:
    domain = None
    codomain = None
    _keys = None

    def __init__(
        self, function=None, domain=None, codomain=None, keys=None, **kwargs
    ):
        if domain is not None:
            self.domain = domain
        elif self.domain is None:
            raise Exception("No domain configured")

        if codomain is not None:
            self.codomain = codomain
        elif self.codomain is None:
            raise Exception("No codomain configured")

        if keys is not None:
            self._keys = keys

        if function is not None:
            if not callable(function):
                raise Exception("Function is not callable")
            else:
                self._set_function(function)

    def _set_function(self, function):
        self._function = cache(function)
        update_wrapper(self, function)

    def __call__(self, *args, _func=None, **kwargs):
        if callable(args[0]) and self._function is None:
            self._set_function(args[0])
            return self

        if self._function is not None:
            nargs = self.domain.from_compatible(*args)
            try:
                _returnable = self._function(*nargs, **kwargs)
            except:
                _returnable = self._function(nargs, **kwargs)
            if _returnable is None:
                raise Exception("Error evaluating function")
            return self.codomain.from_compatible(_returnable)

    def __add__(self, other):
        _new_func, cls = None, None
        if (
            isinstance(other, MathematicalFunction)
            and self.domain != other.domain
        ):
            raise Exception("Incompatible domains")
        if (
            isinstance(other, self.__class__)
            and self.codomain == other.codomain
        ):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) + other(*args, **kwargs)

            cls = self.__class__

        elif self.codomain.is_compatible(other):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) + other

            cls = self.__class__

        elif (
            isinstance(other, tuple(self.__class__.mro())[:-1])
            and self.codomain == other.codomain
        ):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) + other(*args, **kwargs)

            cls = self.__class__

        if _new_func is not None and cls is not None:
            return cls(
                function=_new_func,
                domain=self.domain,
                codomain=self.codomain,
                keys=self._keys,
            )

        raise TypeError(
            f"Unable to perform __add__ between {self.__class__} and {other.__class__}"
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        """
        Scalar x Scalar = Scalar
        Vector x Vector = Scalar

        Scalar x Vector = Vector
        Vector x Scalar = Vector
        """
        _new_func, cls = None, None
        if self.domain != other.domain:
            raise Exception("Incompatible domains")

        if self.codomain.is_compatible(other) or RealNumber.is_compatible(
            other
        ):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) * other

            cls = self.__class__

        if (
            isinstance(other, tuple(self.__class__.mro())[:-1])
            and self.codomain == other.codomain
        ):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) * other(*args, **kwargs)

            cls = self.__class__

        if _new_func is not None and cls is not None:
            return cls(
                function=_new_func,
                domain=self.domain,
                codomain=self.codomain,
                keys=self._keys,
            )

        raise TypeError(
            f"Unable to perform __add__ between {self.__class__} and {other.__class__}"
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        """The substraction should fall directly from the addition
        and multiplication."""
        return self + other * (-1)

    def __rsub__(self, other):
        return ((-1) * self) + other
