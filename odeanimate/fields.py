from odeanimate.meta import MathematicalFunction
from odeanimate.utils import cache, RealNumber
from odeanimate.vector import Vector, Vector2D, Vector3D


class ScalarField(MathematicalFunction):
    domain = Vector
    codomain = RealNumber

    def __truediv__(self, other):
        _new_func = None
        if isinstance(other, ScalarField):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) / other(*args, **kwargs)

        elif RealNumber.is_compatible(other):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) / other

        if _new_func is not None:
            return self.__class__(function=_new_func)
        raise Exception("Can not perform division with non scalar")

    def __rtruediv__(self, other):
        _new_func = None

        if RealNumber.is_compatible(other):

            def _new_func(*args, **kwargs):
                return other / self(*args, **kwargs)

        if _new_func is not None:
            return self.__class__(function=_new_func)
        raise Exception("Can not perform division with non scalar")

    def __pow__(self, other):
        cls, _new_func = ScalarField, None
        if isinstance(other, cls):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) ** other(*args, **kwargs)

        elif RealNumber.is_compatible(other):

            def _new_func(*args, **kwargs):
                return self(*args, **kwargs) ** other

        return cls(function=_new_fuc)


class ScalarField2D(ScalarField):
    """
    Example

        >>> @ScalarField2D
        ... def field(x, y):
        ...     return x * y
        ...
        >>> field(1, 2)
        2
        >>> field((1, 2))
        2
        >>> field(Vector2D(1, 2))
        2
        >>> field(*Vector2D(1, 2))
        2
        >>> field(Vector(1, 2))
        2
        >>> field(*Vector(1, 2))
        2
        >>> @ScalarField2D
        ... def campo(x, y):
        ...     return x / y
        ...
        >>> (field + campo)(1, 1)
        2.0
        >>> (field * campo)(1, 1)
        1.0
        >>> (field / campo)(1, 1)
        1.0
        >>> (field / 2)(1, 1)
        0.5
        >>> (2 / field)(1, 1)
        2.0

    """

    domain = Vector2D
    codomain = RealNumber
