import math
from numbers import Number
from functools import wraps
from odeanimate.utils import dense_range


class Vector:
    def __init__(self, *args, **kwargs):
        """
        >>> Vector(1)
        Vector(1,)
        >>> Vector(1,2)
        Vector(1, 2)
        >>> (*Vector(1,2),)
        (1, 2)
        """
        if isinstance(args[0], self.__class__):
            args = args[0].values
        if any((not isinstance(i, Number) for i in args)):
            raise Exception("Error on args, invalid types.")
        self.dimension = len(args)
        self.values = args

    def __len__(self):
        return self.dimension

    def validation_dimension(self, other):
        if self.dimension != other.dimension:
            raise Exception(f"Object {self} and {other} not compatible dimensions")

    def validation_type(self, other):
        if not isinstance(other, Vector):
            raise Exception(f"Object {self} and {other} not compatible types")

    def euclidean_norm(self):
        return self.norm(p=2)

    def norm(self, p=2):
        return sum(i ** p for i in self.values) ** (1.0 / p)

    def dot(self, right):
        """
        >>> Vector(1, 2, 3).dot(Vector(1, 2, 3))
        14
        """
        self.validation_type(right)
        self.validation_dimension(right)
        return sum(i * j for (i, j) in zip(self.values, right.values))

    def __abs__(self):
        """
        >>> abs(Vector(4, -3))
        5.0
        """
        return self.euclidean_norm()

    def __add__(self, right):
        """
        >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
        >>> a + b
        Vector(3, 4, 5)
        """
        if len(self) == 1 and isinstance(right, Number):
            return Vector(self[0] + right)
        self.validation_type(right)
        self.validation_dimension(right)
        return self.__class__(*[sum(i) for i in zip(self.values, right.values)])

    def __radd__(self, other):
        return self + other

    def __mul__(self, left):
        """
        >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
        >>> a*2
        Vector(2, 2, 2)
        >>> 2*Vector(2)
        Vector(4,)
        >>> 0.5*Vector(2)
        Vector(1.0,)
        >>> Vector(1, 1, 1) * Vector(1, -1, 0)
        0
        >>> Vector(1, 2, 3) * Vector(1, 2, 3)
        14
        """
        if isinstance(left, Number) or (
            isinstance(left, self.__class__) and len(left) == 1
        ):
            return self.__class__(*[left * v for v in self.values])
        if isinstance(left, Vector) and self.dimension == left.dimension:
            return self.dot(left)
        raise Exception(f"Can not operate with {type(left).__name__}")

    def __sub__(self, right):
        return self + (-1) * right

    def __rsub__(self, right):
        return (-1) * self + right

    def __rmul__(self, right):
        """
        >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
        >>> 2*a
        Vector(2, 2, 2)
        >>> a, b = Vector(3), Vector(2)
        >>> b*a
        Vector(6,)
        """
        return self * right

    def __truediv__(self, left):
        """
        >>> Vector(10, 10, 10) / 10
        Vector(1.0, 1.0, 1.0)
        """
        return self * (1 / left)

    def __rtruediv__(self, other):
        if len(self) == 1 and isinstance(other, Number):
            return Vector(other / self[0])
        raise NotImplemented

    def __eq__(self, other):
        returnable = False
        try:
            criteria = [
                self.dimension == other.dimension,
                all((i == j for (i, j) in zip(self.values, other.values))),
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

        def _derivative(t, h=0.001, **kwargs):
            return (new_func(t + h) - new_func(t - h)) / (2 * h)

        new_func.derivative = _derivative
        return new_func


class Vector2D(Vector):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, **kwargs)

    def __str__(self):
        return f"Vector2D{self.values}"

    @property
    def x(self):
        return self.values[0]

    @property
    def y(self):
        return self.values[-1]

    @property
    def angle(self):
        if self.y == self.x == 0:
            return 0
        try:
            return math.atan(self.y / self.x)
        except ZeroDivisionError:
            return 1

    @property
    def _quadrant_tuple(self):
        return (
            "+" if self.x >= 0 else "-",
            "+" if self.y >= 0 else "-",
        )

    @property
    def quadrant(self):
        return {("+", "+"): 1, ("+", "-"): 2, ("-", "-"): 3, ("+", "-"): 4,}[
            self._quadrant_tuple
        ]

    @property
    def i(self):
        return Vector2D(-1 * self.y, self.x)

    @property
    def J(self):
        return self.i

    @classmethod
    def from_vector(cls, vector):
        if isinstance(vector, cls):
            return vector
        elif isinstance(vector, Vector) and vector.dimension == 2:
            return cls(vector[0], vector[1])


class Vector3D(Vector):
    def __init__(self, x, y, z, **kwargs):
        super().__init__(x, y, z, **kwargs)

    def __str__(self):
        return f"Vector3D{self.values}"

    def __matmul__(self, other):
        """
        >>> Vector3D(1, 1, 1) @ Vector3D(1, 1, 1)
        Vector3D(0, 0, 0)
        >>> Vector3D(1, 1, 1) @ Vector3D(1, 0, 1)
        Vector3D(1, 0, -1)
        >>> Vector3D(1, 1, 1) @ Vector3D(1, -1, 1)
        Vector3D(2, 0, -2)
        >>> Vector3D(1, 1, 0) @ Vector3D(1, -1, 1)
        Vector3D(1, -1, -2)
        """
        if not isinstance(self, Vector3D):
            raise Exception("Can not perform cross product")
        s, o = self, other
        return Vector3D(
            s.y*o.z - s.z*o.y,
           -s.x*o.z + s.z*o.x,
            s.x*o.y - s.y*o.x,
        )

    @property
    def x(self):
        return self.values[0]

    @property
    def y(self):
        return self.values[1]

    @property
    def z(self):
        return self.values[2]

    def cross(self, other):
        return self.__class__(
            (self.y * other.z - self.z * other.y),
            -(self.x * other.z - self.z * other.x),
            (self.x * other.y - self.y * other.x),
        )

    @classmethod
    def from_vector(cls, vector):
        if isinstance(vector, cls):
            return vector
        elif isinstance(vector, Vector) and vector.dimension == 2:
            return cls(vector[0], vector[1], vector[2])


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
