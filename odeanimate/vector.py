import math
from functools import wraps


class Vector:

    def __init__(self, *args, **kwargs):
        if any((not isinstance(i, (int, float, complex,)) for i in args)):
            raise Exception(
                "Error on args, invalid types."
            )
        self.dimension = len(args)
        self.values = args

    def __len__(self):
        return self.dimension

    def euclidean_norm(self):
        return math.sqrt(sum(i**2 for i in self.values))


    def dot(self, right):
        if not isinstance(right, self.__class__):
            raise Exception(
                f"No puedes hacer producto punto un tipo {type(right).__name__} con un Vector"
            )
        if self.dimension != right.dimension:
            raise Exception (
                f"No puedes hacer un producto punto entre un Vector de dimension {self.dimension} y un Vector de dimension {right.dimension}"
            )
        return sum(i*j for (i,j) in zip(self.values, right.values))


    def __add__(self, right):
        """
        >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
        >>> a + b
        Vector(3, 4, 5)
        """
        if not isinstance(right, self.__class__):
            raise Exception(
                f"Can not add type {type(right).__name__} with vector."
            )
        if self.dimension != right.dimension:
            raise Exception(
                f"Can not add a vector with dimension {self.dimension} to a vector with dimension {right.dimension}"
            )
        return Vector(*[sum(i) for i in zip(self.values, right.values)])

    def __sub__(self, right):
        if not isinstance(right, self.__class__):
            raise Exception(
                f"Can not sub type {type(right).__name__} with vector"
            )
        if self.dimension != right.dimension:
            raise Exception(
                f"Can not sub a vector with dimension {self.dimension} to a vector with dimension {right.dimension}"
            )
        return Vector(*[(i-j) for (i,j) in zip(self.values, right.values)])

    def __mul__(self, left):
        """
        >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
        >>> a*2
        Vector(2, 2, 2)
        """
        if isinstance(left, (int, float, complex)):
            return Vector(*[left*v for v in self.values])
        raise Exception(
            f"Can not operate with {type(left).__name__}"
        )

    def __rmul__(self, right):
        """
        >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
        >>> 2*a
        Vector(2, 2, 2)
        """
        if isinstance(right, (int, float, complex)):
            return self * right
        raise Exception(
            f"Operación entre {type(right).__name__} y Vector no es posible"
        )

    def __truediv__(self, left):
        if isinstance(left, (int, float, complex)):
            return Vector(*[v/left for v in self.values])
        raise Exception(
            f"Operación entre {type(left).__name__} y Vector no es posible"
        )

    def __eq__(self, other):
        criteria = [
            self.dimension == other.dimension,
            all((i == j for (i, j) in zip(self.values, other.values)))
        ]
        return all(criteria)

    def __getitem__(self, _slice):
        """
        >>> Vector(1,2,3,4,5)[1]
        Vector(2,)
        >>> Vector(1,2,3,4,5)[1:3]
        Vector(2, 3)
        >>> Vector(1,2,3,4,5)[::-1]
        Vector(5, 4, 3, 2, 1)
        >>> Vector(1,2,3,4,5)[::2]
        Vector(1, 3, 5)
        >>> Vector(1,2)["10"]
        Traceback (most recent call last):
          ...
        Exception: Invalid Descriptor.
        """
        if isinstance(_slice, slice):
            return Vector(*self.values[_slice])
        elif isinstance(_slice, int):
            return Vector(self.values[_slice])
        raise Exception("Invalid Descriptor.")

    def __str__(self):
        return f"Vector{self.values}"

    def __repr__(self):
        return str(self)

    @classmethod
    def codomain(cls, func):
        """
        >>> @Vector.codomain
        ... def parabola(t):
        ...     return t, t**2 - 9
        ...
        >>> parabola(2)
        Vector(2, -5)
        """
        @wraps(func)
        def _vector_codomain(*args, **kwargs):
            return Vector(*func(*args, **kwargs))
        return _vector_codomain


if __name__ == '__main__':
    import doctest
    doctest.testmod()
