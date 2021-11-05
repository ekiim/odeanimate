import math
from functools import wraps
from odeanimate.utils import dense_range


class Vector:
    def __init__(self, *args, **kwargs):
        if isinstance(args[0], self.__class__):
            args = args[0].values
        if any((not isinstance(i, (int, float, complex,)) for i in args)):
            raise Exception(
                "Error on args, invalid types."
            )
        self.dimension = len(args)
        self.values = args

    def __len__(self):
        return self.dimension

    def validation_dimension(self, other):
        if len(self) != len(other):
            raise Exception(
                f"Objeto {self} no es de "
                f"la misma dimension que objeto {other}."
            )

    def validation_type(self, other):
        if not isinstance(other, self.__class__):
            raise Exception(
                f"Objeto {other} no es del mismo tipo que "
                f"objeto {self}"
            )

    def euclidean_norm(self):
        return self.norm(p=2)

    def norm(self, p=2):
        return sum(i**p for i in self.values)**(1.0 / p)

    def dot(self, right):
        """
        >>> Vector(1, 2, 3).dot(Vector(1, 2, 3))
        14
        """
        self.validation_type(right)
        self.validation_dimension(right)
        return sum(i*j for (i, j) in zip(self.values, right.values))

    def __abs__(self):
        """
        >>> abs(Vector(4, -3))
        5.0
        """
        return self.euclidean_norm()

    def __matmul__(self, right):
        """
        >>> Vector(1, 2, 3) @ Vector(1, 2, 3)
        14
        """
        return self.dot(right)

    def __add__(self, right):
        """
        >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
        >>> a + b
        Vector(3, 4, 5)
        """
        self.validation_type(right)
        self.validation_dimension(right)
        return self.__class__(*[sum(i) for i in zip(self.values, right.values)])

    def __mul__(self, left):
        """
        >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
        >>> a*2
        Vector(2, 2, 2)
        """
        if isinstance(left, (int, float, complex)):
            return self.__class__(*[left*v for v in self.values])
        raise Exception(
            f"Can not operate with {type(left).__name__}"
        )

    def __sub__(self, right):
        return self + (-1) * right

    def __rmul__(self, right):
        """
        >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
        >>> 2*a
        Vector(2, 2, 2)
        """
        return self * right

    def __truediv__(self, left):
        """
        >>> Vector(10, 10, 10) / 10
        Vector(1.0, 1.0, 1.0)
        """
        return self * (1/left)

    def __eq__(self, other):
        returnable = False
        try:
            criteria = [
                self.dimension == other.dimension,
                all((i == j for (i, j) in zip(self.values, other.values)))
            ]
            returnable = all(criteria)
        except:
            pass
        return returnable

    def __getitem__(self, _slice):
        """
        >>> Vector(1,2,3,4,5)[1]
        2
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
            return self.__class__(*self.values[_slice])
        elif isinstance(_slice, int):
            return self.values[_slice]
        raise Exception("Invalid Descriptor.")

    def __str__(self):
        return f"Vector{self.values}"

    def __repr__(self):
        return str(self)

    def __float__(self):
        if len(self) == 1:
            return float(self.values[0])
        raise Exception("Can not convert vector to number")

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
            return cls(*func(*args, **kwargs))
        return _vector_codomain

    @classmethod
    def curve(cls, func):

        new_func = cls.codomain(func)

        def _range_evaluation(start, end, step=1):
            return VectorCollection(*[
                new_func(t) for t in dense_range(start, end, step)
            ])
        new_func.range = _range_evaluation

        def _derivative(t, h=0.001, **kwargs):
            return (new_func(t + h) - new_func(t - h)) / (2*h)

        new_func.derivative = _derivative

        return new_func


class Vector2D(Vector):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, **kwargs)

    def __str__(self):
        return f"Vector2D{self.values}"

    def x(self):
        return self.values[0]

    def y(self):
        return self.values[-1]

    def i(self):
        return Vector2D(-1*self.y, self.x)

class Vector3D(Vector):
    def __init__(self, x, y, z, **kwargs):
        super().__init__(x, y, z, **kwargs)

    def __str__(self):
        return f"Vector3D{self.values}"

    def x(self):
        return self.values[0]

    def y(self):
        return self.values[1]

    def z(self):
        return self.values[2]

    def cross(self, other):
        return self.__class__(
            (self.y*other.z - self.z*other.y),
            -(self.x*other.z - self.z*other.x),
            (self.x*other.y - self.y*other.x),
        )

class VectorCollection:
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            raise Exception("Empty collection")
        if not all(isinstance(a, Vector) for a in args):
            raise Exception("This are not vectors")
        if not all(len(args[0]) == len(a) for a in args):
            raise Exception("Different dimension vectors")
        self.collection = list(args)
        self.count = len(args)
        self.dimension = len(args[0])

    def __len__(self):
        return self.count

    def __getitem__(self, _slice):
        returnable = self.collection[_slice]
        if isinstance(returnable, list):
            returnable = VectorCollection(*returnable)
        return returnable

    def __iter__(self):
        return iter(self.collection)

    def components(self, *comp):
        if len(comp) == 0:
            comp = list(range(self.dimension))
        return [
            [float(vec[i]) for vec in self.collection]
            for i in comp
        ]


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False)
