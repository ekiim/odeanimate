from numbers import Number
from functools import wraps
from math import acos, atan2
from odeanimate.utils import tolerance


class Vector:
    def __init__(self, *args, **kwargs):
        """
        >>> Vector(1)
        Vector(1,)
        >>> Vector(1,2)
        Vector(1, 2)
        >>> (*Vector(1,2),)
        (1, 2)
        >>> Vector(1, "2")
        Traceback (most recent call last):
          ...
        Exception: Error on args, invalid types.
        """
        if isinstance(args[0], self.__class__):
            args = args[0].values
        if any((not isinstance(i, Number) for i in args)):
            raise Exception("Error on args, invalid types.")
        self.dimension = len(args)
        self.values = args
        self.origin = kwargs.get("origin", None)
        if self.origin is not None and not isinstance(self.origin, (self.__class__)):
            raise TypeError("Unsupported origin for the vector")

    def __len__(self):
        return self.dimension

    def validation_dimension(self, other):
        """
        >>> Vector(1, 2).validation_dimension(Vector(1, 2, 3))
        Traceback (most recent call last):
          ...
        Exception: Object Vector(1, 2) and Vector(1, 2, 3) not compatible dimensions
        """
        if self.dimension != other.dimension:
            raise Exception(f"Object {self} and {other} not compatible dimensions")

    def validation_type(self, other):
        """
        >>> Vector(1, 2).validation_type("STRING")
        Traceback (most recent call last):
          ...
        Exception: Object Vector(1, 2) and STRING not compatible types
        """
        if not isinstance(other, Vector):
            raise Exception(f"Object {self} and {other} not compatible types")

    def euclidean_norm(self):
        return self.norm(p=2)

    def norm(self, p=2):
        return sum(abs(i) ** p for i in self.values) ** (1.0 / p)

    def dot(self, right):
        """
        >>> Vector(1, 2, 3).dot(Vector(1, 2, 3))
        14
        """
        self.validation_type(right)
        self.validation_dimension(right)
        return sum(i * j for (i, j) in zip(self.values, right.values))

    @property
    def direction(self):
        return self / abs(self)

    def angle_with(self, other):
        """
        >>> from math import pi
        >>> Vector(0,1).angle_with(Vector(0, -1)) == pi
        True
        >>> Vector(0,1).angle_with(Vector(1, 0)) == pi / 2
        True
        >>> (Vector(1,1).angle_with(Vector(1, 0)) - pi / 4) < tolerance
        True
        """
        a, b = self.direction, other.direction
        return abs(acos(a * b))

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
        >>> Vector(1, 2, 3, 4) + Vector(4, 3, 2, 1)
        Vector(5, 5, 5, 5)
        >>> Vector(1) + 1
        Vector(2,)
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
        >>> Vector(1, 2, 3, 4)*3
        Vector(3, 6, 9, 12)
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
        if isinstance(left, Number):
            return self * (1 / left)
        raise TypeError("Can not divide by a non number")

    def __rtruediv__(self, other):
        if len(self) == 1 and isinstance(other, Number):
            return Vector(other / self[0])
        return NotImplemented

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

    def _repr_latex_(self):
        return "".join(["$(", ",".join(map(str, self)), ")$"])


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
        return atan2(self.y, self.x)

    @property
    def angle_full(self):
        # offset = pi * ((self.quadrant-1) // 2)
        offset = 0
        return self.angle + offset

    @property
    def _quadrant_tuple(self):
        return (
            "+" if self.x >= 0 else "-",
            "+" if self.y >= 0 else "-",
        )

    @property
    def quadrant(self):
        return {
            ("+", "+"): 1,
            ("+", "-"): 2,
            ("-", "-"): 3,
            ("-", "+"): 4,
        }[self._quadrant_tuple]

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

    @classmethod
    def from_complex(cls, z):
        return Vector2D(z.real, z.imag)

    def _plot_2d(self, ax, point=False, origin=None, **kwargs):
        if point:
            ax.scatter([self.x], [self.y])
        else:
            if self.origin:
                origin = self.origin
            elif isinstance(origin, self.__class__):
                pass
            else:
                origin = self.__class__(0, 0)
            ax.quiver(
                [origin.x],
                [origin.y],
                [self.x],
                [self.y],
                angles="xy",
                scale_units="xy",
                scale=1,
            )


class Vector3D(Vector):
    def __init__(self, x, y, z, **kwargs):
        super().__init__(x, y, z, **kwargs)

    def __str__(self):
        return f"Vector3D{self.values}"

    def __xor__(self, other):
        """
        >>> Vector3D(1, 1, 1) ^ Vector3D(1, 1, 1)
        Vector3D(0, 0, 0)
        >>> Vector3D(1, 1, 1) ^ Vector3D(1, 0, 1)
        Vector3D(1, 0, -1)
        >>> Vector3D(1, 1, 1) ^ Vector3D(1, -1, 1)
        Vector3D(2, 0, -2)
        >>> Vector3D(1, 1, 0) ^ Vector3D(1, -1, 1)
        Vector3D(1, -1, -2)
        """
        if not isinstance(self, Vector3D):
            raise Exception("Can not perform cross product")
        s, o = self, other
        return Vector3D(
            s.y * o.z - s.z * o.y,
            -s.x * o.z + s.z * o.x,
            s.x * o.y - s.y * o.x,
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

    def _plot_3d(self, ax, point=False, origin=None, **kwargs):
        if point:
            ax.scatter([self.x], [self.y], [self.z])
        else:
            if self.origin:
                origin = self.origin
            elif isinstance(origin, self.__class__):
                pass
            else:
                origin = self.__class__(0, 0, 0)
            ax.quiver(
                [origin.x],
                [origin.y],
                [origin.z],
                [self.x],
                [self.y],
                [self.z],
            )

    def to_2D(self):
        return Vector2D(self.x, self.y)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
