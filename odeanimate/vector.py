"""
# Vector Objects

In mathematics vector has strictly speaking one meaining, an element of a vector space, but
in a more pragmatic look, we usually call a vector to an _arrow from one point to another in the
euclidean space_, and most of the geometry can be describe by analyzing the geometry
from the euclidean through undrestanding functions that map from it to a given object.

In this module we will deal with vectors in the most simple way possible, in an almost naive way.

A `Vector` is a programing object which is an instance of the `Vector` class, (there are also
sub classes for 2 and 3 dimensional vectors implementing the basics for them).

There is some to say about this objects, so I would recomend reading this document by following it
as if each method or class definition is a _lemma_.
"""

from functools import wraps
from math import acos, atan2
from odeanimate.array import Array
from odeanimate.utils import tolerance, RealNumber


class Vector(Array):
    """Vector base class

    The methods implemented here apply to any other type of vector, which
    means that is inheriting directly or indirectly from this class.
    """

    def __init__(self, *args, **kwargs):
        """
        The construction of vectors is done by providing a series of
        numerical values, which could be any python object that
        check with the standard base class `numbers.Real`.

        > Support for complex numbers exists but has not been actually tested, but
        > in priciple it should work, except for some edge cases.

        You can provide a list of numbers as follows.

            >>> Vector(1)
            Vector(1,)
            >>> Vector(1,2)
            Vector(1, 2)

        Since it is read by the arbirary positional argument, it should be
        ready to go, from `list` or `tuples` to `Vector`.

            >>> a = (1, 2, 3)
            >>> Vector(*a)
            Vector(1, 2, 3)

        Also once the object exists, you can unpack it with out an issue.

            >>> (*Vector(1,2),)
            (1, 2)

        Python and this module are smart, but not smart enough (like javascript),
        to interpret string values as numbers.

            >>> Vector(1, "2")
            Traceback (most recent call last):
              ...
            Exception: Invalid types on values of input structure.
        """
        super().__init__(*args, **kwargs)
        self.origin = kwargs.get("origin", None)
        self.dimension = self.shape[0]
        if self.origin is not None and not isinstance(
            self.origin, (self.__class__)
        ):
            raise TypeError("Unsupported origin for the vector")

    def __len__(self):
        """
        Asking for the length of a vector, will provide you with the dimension.

        > Listening to this, might seem odd, but having `abs` to define the actual
        > length by calculating the norm makes more sense.

            >>> len(Vector(1, 2))
            2
            >>> len(Vector(1, 2, 3))
            3
        """
        return self.dimension

    def validation_dimension(self, other):
        """
        This is a helper method, used internally to validate prior making an
        operation between two vectors that requires the same dimension.

        > Possible hide this by adding an underscore to the function.
        > Discussion required.

            >>> Vector(1, 2).validation_dimension(Vector(1, 2, 3))
            Traceback (most recent call last):
              ...
            Exception: Object Vector(1, 2) and Vector(1, 2, 3) not compatible dimensions
        """
        if self.dimension != other.dimension:
            raise Exception(
                f"Object {self} and {other} not compatible dimensions"
            )

    def validation_type(self, other):
        """
        This is a helper method, used internally to validate prior making an
        operation between two objects requiring the same type.

        > Possible hide this by adding an underscore to the function.
        > Discussion required.

            >>> Vector(1, 2).validation_type("STRING")
            Traceback (most recent call last):
              ...
            Exception: Object Vector(1, 2) and STRING not compatible types
        """
        if not isinstance(other, Vector):
            raise Exception(f"Object {self} and {other} not compatible types")

    def norm(self, p=2):
        """
        This method will allow you to calculate the $p$ norm.
        You can pass a single argument to specify which $p$ value, defaulted
        to $p=2$.
        """
        return sum(abs(i) ** p for i in self) ** (1.0 / p)

    def euclidean_norm(self):
        """
        Providing an alias for the $p=2$ norm.
        """
        return self.norm(p=2)

    def dot(self, right):
        """
        The dot product, inner product or euclidean product is accesible as a
        method, or also can be used by direct multiplication operator.

            >>> Vector(1, 2, 3).dot(Vector(1, 2, 3))
            14
            >>> a, b = Vector(1, 2, 3), Vector(1, 2, 3)
            >>> a.dot(b) == a*b
            True
        """
        self.validation_type(right)
        self.validation_dimension(right)
        return sum(i * j for (i, j) in zip(self, right))

    @property
    def direction(self):
        """
        This is a calculated property, not a method, you can access the direction
        of a vector by just asking for the `direction` property.
        (It can not be set.)
        """
        return self / abs(self)

    def angle_with(self, other):
        """
        This method, will allow you to calculate the angle between two vectors,
        the calculation is done by using the inner product formula for deducing
        the angle.

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
        Calculating the `abs` (absolute value), will provide you with the
        actual length or norm of the vector.

            >>> abs(Vector(4, -3))
            5.0
        """
        return self.euclidean_norm()

    def __add__(self, right):
        """
        This method will allow the user to add vectors,
        aslong as they are compatible with each other.

        > Technically this method will only get executed
        > when you attempt to sum a vector with something
        > by the right side.
        > Let's say $V$ is this object, and $W$ is some
        > other vector that we want to add to $V$
        > Doing `V + W` is equivalent to doing
        > `V.__add__(W)`.


            >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
            >>> a + b
            Vector(3, 4, 5)
            >>> Vector(1, 2, 3, 4) + Vector(4, 3, 2, 1)
            Vector(5, 5, 5, 5)
            >>> Vector(1) + 1
            Vector(2,)
        """
        if len(self) == 1 and RealNumber.is_compatible(right):
            return Vector(self[0] + right)
        self.validation_type(right)
        self.validation_dimension(right)
        return self.__class__(*[sum(i) for i in zip(self, right)])

    def __radd__(self, other):
        """
        This method exists to allow left hand side addition, and assuming they
        commutation, this should work fine.
        > Let's say $V$ is this object, and $W$ is some
        > other object that we want to add to $V$
        > Doing `W + V` is equivalent to doing
        > `V.__radd__(W)`.
        > This method will only kick in if the object $W$, does not
        > support addition with an object of this kind.

            >>> 1 + Vector(1)
            Vector(2,)

        Like in the previous example, the `int` type does not support
        addition with `Vector` objects, but we do want to allow this.

        """
        return self + other

    def __mul__(self, left):
        """
        Vector multiplication is defined as the inner product when we are
        doing it against another of the same dimension.


            >>> a, b = Vector(1, 1, 1), Vector(2, 3, 4)
            >>> a*2
            Vector(2, 2, 2)
            >>> Vector(1, 1, 1) * Vector(1, -1, 0)
            0
            >>> Vector(1, 2, 3) * Vector(1, 2, 3)
            14
            >>> a, b = Vector(3), Vector(2)
            >>> b*a
            Vector(6,)

        Also we need tu support scalar multiplication.

            >>> Vector(1, 2, 3, 4)*3
            Vector(3, 6, 9, 12)

        """
        if RealNumber.is_compatible(left) or (
            isinstance(left, self.__class__) and len(left) == 1
        ):
            return self.__class__(*[left * v for v in self])
        if isinstance(left, Vector) and self.dimension == left.dimension:
            return self.dot(left)
        raise Exception(f"Can not operate with {type(left).__name__}")

    def __rmul__(self, right):
        """

        What we had in the previos method was not full scalar multiplication,
        it was only right scalar multiplication.

        Right here we allow for numbers to be multiplied by vectors,
        hence allowing the scalar multiplication from both sides.

            >>> a = Vector(1, 1, 1)
            >>> 2*a
            Vector(2, 2, 2)
            >>> 2*Vector(2)
            Vector(4,)
            >>> 0.5*Vector(2)
            Vector(1.0,)

        > This methods actually fall back to the regular multiplication definition,
        after commuting the elements.
        """
        return self * right

    def __sub__(self, right):
        """
        The substraction, it falls directly from having defined the `__add__`, and `__rmul__`, by using
        the following formula $v - w = v + (-1)*w$.
        """
        return self + (-1) * right

    def __rsub__(self, right):
        """
        This method will get executed when whatever object is trying to substract this vector from it,
        does not know how to.

        > Technical opinion required here.
        """
        return (-1) * self + right

    def __truediv__(self, left):
        """
        This method is defined to allow division by scalras, which essentialy
        is multiplying by the the reciprocal of a number. (actually that is how
        it's implemented)

            >>> Vector(10, 10, 10) / 10
            Vector(1.0, 1.0, 1.0)
        """
        if RealNumber.is_compatible(left):
            return self * (1 / left)
        raise TypeError("Can not divide by a non number")

    def __rtruediv__(self, other):
        """
        > Discussion required, this method, is to allow object
        > divided by vector, but the only way this is allowed
        > if it is a _one dimensional_ vector.
        """
        if len(self) == 1 and RealNumber.is_compatible(other):
            return Vector(other / self[0])
        return NotImplemented

    def __eq__(self, other):
        """
        This method is to allow comparison between numbers
        > Discussion required
        >
        > Due floting point arithmetic, this method might fail, because
        > it's attempting to compare each component for equality.
        > May be returning something like
        > If the length difference between two vectors is close enough to zero.
        >
        """
        returnable = False
        try:
            criteria = [
                self.dimension == other.dimension,
                all((i == j for (i, j) in zip(self, other))),
            ]
            returnable = all(criteria)
        except:
            pass
        return returnable

    def __getitem__(self, _slice):
        """
        This is the  behaviour used for when accesing with descriptors.

        > A descriptor is what you put between square brackets, when accesing a list
        element or a dictionary value by key.

        It should pretty much work as one would expect for lists.

        A couple of examples ahead.

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
            return self.__class__(*super().__getitem__(_slice))
        elif isinstance(_slice, int):
            return super().__getitem__(_slice)
        raise Exception("Invalid Descriptor.")

    def __str__(self):
        """This is the string representation of a vector)"""
        return f"{self.__class__.__name__}{self._array}"

    def __repr__(self):
        """This is the "terminal" representation of a vector)"""
        return str(self)

    def __float__(self):
        """
        This method only works, when you are trying to convert a one dimensional
        to  number.
        """
        if len(self) == 1:
            return float(self[0])
        raise Exception("Can not convert Vector to float or number.")

    def _repr_latex_(self):
        """
        This method is to write a vector as latex, used for jupyter notebooks.
        """
        return "".join(["$(", ",".join(map(str, self)), ")$"])

    @classmethod
    def from_vector(cls, vector):
        if isinstance(vector, cls):
            return vector
        raise Exception("Not a vector")

    @classmethod
    def codomain(cls, func):
        """

        > _To be Deprecated_

            >>> @Vector.codomain
            ... def parabola(t):
            ...     return t, t**2 - 9
            ...
            >>> parabola(2)
            Vector(2, -5)

        Files that use this:

            - examples/plots-isoclines-examples-with-solution.py
            - examples/plots-isoclines-examples.py
            - examples/plots-isoclines-orthogonal-curves-solutions.py
            - examples/plots-isoclines-orthogonal-curves.py
            - examples/plots-isoclines.py
            - examples/vector-curve-function.py

        """

        @wraps(func)
        def _vector_codomain(*args, **kwargs):
            return cls(*func(*args, **kwargs))

        return _vector_codomain

    @classmethod
    def is_compatible(cls, *value):
        if len(value) == 1 and isinstance(value[0], cls):
            return True
        return all((RealNumber.is_compatible(v) for v in value))

    @classmethod
    def from_compatible(cls, *object):
        if len(object) == 1 and isinstance(object[0], cls):
            return cls.from_vector(object[0])
        if len(object) == 1 and isinstance(object[0], (tuple, list)):
            return cls(*object[0])
        try:
            return cls(*object)
        except:
            pass
        try:
            return cls(object)
        except:
            pass
        raise Exception(
            f"Object {object} not compatible with {cls.__name__} class"
        )


"""
## Particular cases

The most common vectors, are two and three dimensions (maybe for when doing
relativity).

Ahead we are showing the Vectors with particular features for two and three dimensions.

"""


class Vector2D(Vector):
    """
    The two dimensional vector, will require only two values for it's construction $x$ and $y$.

        >>> Vector2D(1, 1)
        Vector2D(1, 1)

    """

    def __init__(self, x, y=None, **kwargs):
        if isinstance(x, Vector):
            x, y = x
        super().__init__(x, y, **kwargs)

    def __len__(self):
        """
        It should be expected to return a two as the dimension

        > Discussion requried, check the base clase method for this.
        """
        return 2

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[-1]

    @property
    def angle(self):
        """
        Discussion required, check the details for `atan2` implementation.
        """
        return atan2(self.y, self.x)

    @property
    def angle_full(self):
        """
        The idea of this method is to return a positive angle, to compensate from
        the negative values of the codomain for `atan2`.
        """
        # offset = pi * ((self.quadrant-1) // 2)
        offset = 0
        return self.angle + offset

    @property
    def _quadrant_tuple(self):
        """
        Return a tuple with signs to indicate quadrant of the vector.
        """
        return (
            "+" if self.x >= 0 else "-",
            "+" if self.y >= 0 else "-",
        )

    @property
    def quadrant(self):
        """
        Return the number of quadrant where the vector is located.
        """
        return {
            ("+", "+"): 1,
            ("+", "-"): 2,
            ("-", "-"): 3,
            ("-", "+"): 4,
        }[self._quadrant_tuple]

    @property
    def i(self):
        """
        Apply a multiplication by $i$ complex value to the vector.

        Essentially it should shift the components, and do negative the first.

            >>> Vector2D(1, 2).i
            Vector2D(-2, 1)
        """
        return Vector2D(-1 * self.y, self.x)

    @property
    def J(self):
        """
        See $i$ method above.
        """
        return self.i

    @classmethod
    def from_vector(cls, vector):
        """
        This method will create a two dimensional vector from a vector of dimension two.
        The difference is that you might have a vector which was generated as a vector
        with the base class, with out specifying "this is a two dimensional", and it will
        not be gifted with the methods here.

            >>> Vector2D.from_vector(Vector(1, 2))
            Vector2D(1, 2)
            >>> Vector2D.from_vector(Vector2D(1, 2))
            Vector2D(1, 2)
        """
        if isinstance(vector, cls):
            return vector
        elif isinstance(vector, Vector) and vector.dimension == 2:
            return cls(vector[0], vector[1])

    @classmethod
    def from_complex(cls, z):
        """
        This method is to create a Vector2D from a complex number.
            >>> Vector2D.from_complex(1 + 1j)
            Vector2D(1.0, 1.0)
        """
        return cls.from_compatible(z.real, z.imag)

    @classmethod
    def is_compatible(cls, *value):
        if len(value) == 2 and all(
            [RealNumber.is_compatible(x) for x in value]
        ):
            return True
        return NotImplemented

    def _plot_2d(self, ax, point=False, origin=None, **kwargs):
        """
        This method is exclusively for use from the plotting mechanism, inside of the module.
        """
        mpl_kwargs = {}
        if "color" in kwargs:
            mpl_kwargs["color"] = kwargs["color"]
        if point:
            ax.scatter([self.x], [self.y], **mpl_kwargs)
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
                **mpl_kwargs,
            )


class Vector3D(Vector):
    """
    The three dimensional vector, will require only three values for it's construction $x$, $y$, and $z$.

        >>> Vector3D(1, 1, 1)
        Vector3D(1, 1, 1)

    """

    def __init__(self, x, y=None, z=None, **kwargs):
        if isinstance(x, Vector):
            x, y, z = x
        super().__init__(x, y, z, **kwargs)

    def __len__(self):
        return 3

    def cross(self, other):
        """
        The cross product method.
        """
        if isinstance(other, Vector3D):
            return self.__class__(
                (self.y * other.z - self.z * other.y),
                -(self.x * other.z - self.z * other.x),
                (self.x * other.y - self.y * other.x),
            )
        raise Exception("Invalid cross product between vectors")

    def __xor__(self, other):
        """
        The `xor` operator is `^`, which resembles the wedge symbol $\wedge$, which in three dimensions
        matches the cross product, hence, we are implementing the cross product with that.

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
        return self.cross(other)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @classmethod
    def from_vector(cls, vector):
        if isinstance(vector, cls):
            return vector
        elif isinstance(vector, Vector) and vector.dimension == 2:
            return cls(vector[0], vector[1], vector[2])

    @classmethod
    def is_compatible(cls, *value):
        if len(value) == 3 and all(
            [RealNumber.is_compatible(x) for x in value]
        ):
            return True
        return NotImplemented

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
