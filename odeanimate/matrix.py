from math import sin, cos
from numbers import Number
from odeanimate.utils import slice_to_range, tolerance
from odeanimate.array import Array
from odeanimate.vector import Vector


class Matrix(Array):
    def __init__(self, *rows, shape=None, **kwargs):  # pylint: disable=W0613
        rows_count = len(rows)
        column_count = len(rows[0])
        if shape is None:
            if any(filter(lambda row: len(row) != column_count, rows)):
                raise Exception("Inconsistent columns")
            self._shape = (rows_count, column_count)
        else:
            self._shape = shape
        self.array = []
        for row in rows:
            self.array.extend(row)
        self.array = tuple(self.array)

    @property
    def shape(self):
        return self._shape

    def __repr__(self):
        """
        >>> Matrix((1,), shape=(1,1))
        <Matrix shape=(1, 1) rows=(Vector(1,))>
        >>> Matrix((1,2), shape=(1, 2))
        <Matrix shape=(1, 2) rows=(Vector(1, 2))>
        >>> Matrix((1,2), shape=(2, 1))
        <Matrix shape=(2, 1) rows=(Vector(1,), Vector(2,))>
        """
        rows = ", ".join([repr(self[i]) for i in range(0, self.shape[0])])
        return f"<Matrix shape={self.shape} rows=({rows})>"

    def __getitem__(self, key):
        """
        >>> Matrix([1,2])[0,0]
        1
        >>> Matrix([1], [2])[0,0]
        1
        >>> Matrix([1], [2])[1,0]
        2
        >>> Matrix([1,2],[3,4])[0,0]
        1
        >>> Matrix([1,2],[3,4])[0,1]
        2
        >>> Matrix([1,2],[3,4])[1,0]
        3
        >>> Matrix([1,2],[3,4])[1,1]
        4
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[1,1]
        5
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[2,2]
        9
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[1,2]
        6
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[0]
        Vector(1, 2, 3)
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[0,:]
        Vector(1, 2, 3)
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[1,:]
        Vector(4, 5, 6)
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[:,0]
        Vector(1, 4, 7)
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[:,1]
        Vector(2, 5, 8)
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[:,:2] == Matrix([1,2],[4,5],[7,8])
        True
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[:2,:2] == Matrix([1,2],[4,5])
        True
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[0:2,::2] == Matrix([1,3],[4,6])
        True
        >>> Matrix([1,2,3],[4,5,6],[7,8,9])[0::2,::2] == Matrix([1,3],[7,9])
        True
        >>> Matrix([1,2,3],[4,5,6],[7,8,9],[1,2,3],[4,5,6],[7,8,9])[:,0]
        Vector(1, 4, 7, 1, 4, 7)
        >>> Matrix([1,2,3],[4,5,6],[7,8,9],[1,2,3],[4,5,6],[7,8,9])[:,1]
        Vector(2, 5, 8, 2, 5, 8)
        """
        if not isinstance(key, tuple):
            key = (key, slice(None))
        if isinstance(key, tuple) and len(key) == 2:
            row, col = key
            if isinstance(row, int) and isinstance(col, int):
                pos = self._cell_position_to_array_pos(row, col)
                return self.array[pos]
            if isinstance(row, int) and isinstance(col, slice):
                c_range = slice_to_range(col, self.shape[1])
                r = row
                return Vector(*[self[r, c] for c in c_range])
            if isinstance(row, slice) and isinstance(col, int):
                r_range = slice_to_range(row, self.shape[0])
                c = col
                return Vector(*[self[r, c] for r in r_range])
            if isinstance(row, slice) and isinstance(col, slice):
                r_range = slice_to_range(row, self.shape[0])
                c_range = slice_to_range(col, self.shape[1])
                new_shape = len(r_range), len(c_range)
                cells = [(r, c) for r in r_range for c in c_range]
                return Matrix([self[i, j] for i, j in cells], shape=new_shape)

    def __add__(self, other):
        if not isinstance(other, Matrix) or self.shape != other.shape:
            raise Exception("Inconsistent Sum")
        return Matrix(
            *[a + b for a, b in zip(self.array, other.array)], shape=self.shape
        )

    @property
    def rows(self):
        return tuple(self[i] for i in range(self.shape[0]))

    @property
    def columns(self):
        return tuple(self[:, i] for i in range(self.shape[1]))

    def __mul__(self, other):
        """
        >>> Matrix([1, 0], [0, 1]) * Matrix([0, 1], [1, 0]) ==  Matrix([0, 1], [1, 0])
        True
        >>> Matrix([1, 2]) * Matrix([0, 1], [1, 0]) ==  Matrix([2, 1])
        True
        >>> Matrix([1, 0], [0, 1]) * Vector(2, 2)
        Vector(2, 2)
        >>> Matrix([1, 0, 0], [0, 1, 0]) * Vector(2, 2, 2)
        Vector(2, 2)
        >>> Matrix([1, 0], [0, 1]) * 2
        <Matrix shape=(2, 2) rows=(Vector(2, 0), Vector(0, 2))>
        """
        if isinstance(other, Matrix) and self.shape[1] == other.shape[0]:
            new_shape = self.shape[0], other.shape[1]
            return Matrix(
                [a.dot(b) for a in self.rows for b in other.columns],
                shape=new_shape,
            )
        if isinstance(other, Vector) and self.shape[1] == other.dimension:
            return Vector(
                *[other.dot(a) for a in self.rows],
            )
        if isinstance(other, Number):
            return Matrix([x * other for x in self.array], shape=self.shape)
        raise Exception(
            f"Unsoported Operation betwee Matrix and {other.__class__}"
        )

    def __rmul__(self, other):
        """
        >>> 2*Matrix([1, 0], [0, 1])
        <Matrix shape=(2, 2) rows=(Vector(2, 0), Vector(0, 2))>
        """
        if isinstance(other, Number):
            return self * other
        raise NotImplementedError

    def __call__(self, x):
        return self * x

    def _cell_position_to_array_pos(self, row, col):
        return row * self.shape[1] + col

    def _descriptor_to_cell_positions(self, row, col):
        rows = slice_to_range(row) if isinstance(row, slice) else [row]
        cols = slice_to_range(col) if isinstance(col, slice) else [col]
        return [
            self._cell_position_to_array_pos(i, j) for i in rows for j in cols
        ]

    def __eq__(self, other):
        """
        >>> Matrix([1]) == Matrix([1 + 1e-1000000])
        True
        >>> Matrix([1, 2]) == Matrix([1, 2])
        True
        """
        return self.shape == other.shape and all(
            (abs(a - b) < tolerance for a, b in zip(self.array, other.array))
        )

    def transpose(self):
        """
        >>> Matrix([1, 2]).transpose()
        <Matrix shape=(2, 1) rows=(Vector(1,), Vector(2,))>
        >>> Matrix([1], [2]).transpose() == Matrix([1, 2])
        True
        >>> Matrix([1], [2]).transpose().transpose() == Matrix([1], [2])
        True
        >>> Matrix([1, 2, 3], [4, 5, 6]).transpose().shape
        (3, 2)
        >>> Matrix([1, 2, 3], [4, 5, 6]).transpose() == Matrix([1, 2],[ 3, 4],[5, 6])
        True
        """
        return Matrix(self.array, shape=self.shape[::-1])

    @classmethod
    def Rotation2D(cls, theta=0):
        c, s = cos(theta), sin(theta)
        return cls([c, -s], [s, c])


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
