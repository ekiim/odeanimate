import sys
from itertools import chain, product
from functools import reduce


from odeanimate.utils import RealNumber, mul


class _ArrayHTMLDisplay:
    _html_styles_table = (
        'style="margin: 1em; table-layout: fixed; max-width: 100%;"'
    )
    _html_styles_cell = 'style="border:1px solid black; text-align: center"'
    _html_styles_header = 'style="text-align: center"'
    _html_axis = False

    def _html_format_element(self, element):
        return str(element)

    def _repr_html_row_from_index(self, start, length):
        a = self._array
        styles = self._html_styles_cell
        returnable = (
            "<tr>",
            *[
                f"<td {styles}>{self._html_format_element(a[i])}</td>"
                for i in range(start, length + start)
            ],
            "</tr>",
        )
        return returnable

    def _get_column_name(self, index):
        return index

    def _html_table_header_row_for_columns(self, cols, one_dimensional=False):
        styles = self._html_styles_header
        returnable = (
            "<tr>",
            "" if one_dimensional else "<th></th>",
            *[
                f"<th {styles}>{self._get_column_name(i)}</th>"
                for i in range(cols)
            ],
            "</tr>",
        )
        return returnable

    def _repr_html_(self):
        returnable = []
        if len(self._shape) == 1:
            cols = self._shape[0]
            if self._html_axis:
                returnable.extend(
                    self._html_table_header_row_for_columns(cols, True)
                )
            returnable.extend(self._repr_html_row_from_index(0, cols))

        if len(self._shape) == 2:
            rows, cols = self._shape
            if self._html_axis:
                returnable.extend(self._html_table_header_row_for_columns(cols))
            for row in range(rows):
                extendable = self._repr_html_row_from_index(row * cols, cols)
                if self._html_axis:
                    extendable = (
                        extendable[0],
                        f"<th {self._html_styles_header}>{row}</th>",
                        *extendable[1:],
                    )
                returnable.extend(extendable)
        return "".join(
            (
                f"<table {self._html_styles_table}>",
                *returnable,
                "</table>",
            )
        )


class Array(_ArrayHTMLDisplay):
    _type = RealNumber

    def __init__(self, *args, shape=None, flat_input=False, **kwargs):
        self._shape = (
            self._input_shape_extractor(args) if shape is None else tuple(shape)
        )
        if not flat_input and not self._input_shape_consistent(
            args, self._shape
        ):
            raise Exception("Inconsistent shape of input structure")

        if flat_input:
            self._array = args[0]
        else:
            self._array = tuple(self._flatten_structure(args, self._shape))

        if any(
            (not self.__class__._type.is_compatible(i) for i in self._array)
        ):
            del self._array
            raise Exception("Invalid types on values of input structure.")

        if len(self._array) != mul(self._shape):
            raise Exception("Inconsistency in shape and array element count.")

    def _repr_data(self):
        return f"shape={self._shape}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._repr_data()}>"

    @classmethod
    def _key_element_to_range(cls, element, limit):
        if isinstance(element, slice):
            start = element.start
            stop = element.stop
            step = element.step or 1
        elif isinstance(element, int):
            start = element
            stop = element + 1
            step = 1
        if step < 0:
            if start is None:
                start = limit
            if stop is None:
                stop = -1
        elif step > 0:
            if start is None:
                start = 0
            if stop is None:
                stop = limit + 1
        else:
            raise Exception("Step can not be 0")

        return range(start, stop, step)

    @classmethod
    def _get_flat_index(cls, shape, keys, skip_validation=False):
        valid_acces_key = skip_validation or all(
            (key < limit for key, limit in zip(keys, shape))
        )
        if not valid_acces_key:
            raise IndexError("Index out of bound.")
        index = 0
        for i, k in enumerate(keys):
            index += k * mul(shape[i + 1 :])
        return index

    def __getitem__(self, keys):
        """
        >>> A = Array(range(3), range(3, 6))
        >>> A[0, 0]
        0
        >>> A[0, 1]
        1
        >>> A[0, 2]
        2
        >>> A[1, 0]
        3
        >>> A[1, 1]
        4
        >>> A[1, 2]
        5
        >>> B = Array(range(3), range(3, 6), range(6, 9))
        >>> B[2, 0]
        6
        >>> B[0, 2]
        2
        >>> B[1, 2]
        5
        >>> B[2, 2]
        8
        """
        if not hasattr(keys, "__len__"):
            keys = (keys,)
        if len(keys) != len(self._shape):
            raise Exception("Insufficient values in descriptor.")

        only_numbers_or_slices = all(
            map(
                lambda _slice: isinstance(_slice, int)
                or isinstance(_slice, slice),
                keys,
            )
        )
        if not only_numbers_or_slices:
            raise KeyError(
                "Invalid access descriptor, only admit int or slice."
            )

        only_numbers = all(map(lambda _slice: isinstance(_slice, int), keys))

        if only_numbers:
            index = Array._get_flat_index(self._shape, keys)
            return self._array[index]

        sliced_keys = [
            self.__class__._key_element_to_range(element, limit - 1)
            for (element, limit) in zip(keys, self._shape)
        ]
        _sub_array_indexes = list(
            map(
                lambda key: self.__class__._get_flat_index(self._shape, key),
                product(*sliced_keys),
            )
        )
        _sub_array_shape = tuple(
            len(r)
            for i, r in enumerate(sliced_keys)
            if not isinstance(keys[i], int)
        )
        _sub_array = [self._array[i] for i in _sub_array_indexes]

        return Array(
            _sub_array,
            shape=_sub_array_shape,
            flat_input=True,
        )

    @property
    def shape(self):
        return self._shape

    def __len__(self):
        return mul(self.shape)

    def reshape(self, shape):
        if len(self) != mul(shape):
            raise Exception("Invalid shape")
        return self.__class__(
            self._array,
            shape=shape,
            flat_input=True,
        )

    def transpose(self, i, j):
        index_amount = len(self.shape)
        if i >= index_amount or j >= index_amount:
            raise Exception("Invalid index to swap")
        shape = list(self._shape)
        shape[i], shape[j] = shape[j], shape[i]
        return self.__class__(
            self._array,
            shape=shape,
            flat_input=True,
        )

    @classmethod
    def _has_len_or_none(cls, arg):
        try:
            return len(arg)
        except TypeError:
            pass
        return None

    @classmethod
    def _input_shape_extractor(cls, args):
        """
        >>> Array._input_shape_extractor([0])
        (1,)
        >>> Array._input_shape_extractor([0, 0])
        (2,)
        >>> Array._input_shape_extractor([[0, 0]])
        (1, 2)
        >>> Array._input_shape_extractor([[0, 0], [0, 0]])
        (2, 2)
        >>> Array._input_shape_extractor([[0, 0], [0]])
        (2, 2)
        >>> Array._input_shape_extractor([[0, 0], [0, 0], [0, 0]])
        (3, 2)
        >>> Array._input_shape_extractor([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        (3, 3)
        >>> Array._input_shape_extractor([[0, 0, 0], [0, 0], [0, 0]])
        (3, 3)
        >>> Array._input_shape_extractor([[[0], 0, 0], [0, 0, 0], [0, 0, 0]])
        (3, 3, 1)
        >>> Array._input_shape_extractor([[[0, 0], 0, 0], [0, 0, 0], [0, 0, 0]])
        (3, 3, 2)
        >>> Array._input_shape_extractor((range(1, 4), range(4, 7)))
        (2, 3)
        >>> Array._input_shape_extractor((range(1, 4), range(4, 7), range(7, 10)))
        (3, 3)
        """
        length = cls._has_len_or_none(args)
        if length:
            nested_result = tuple(
                filter(
                    lambda x: x is not None, cls._input_shape_extractor(args[0])
                )
            )
        else:
            nested_result = []
        return (length, *nested_result)

    @classmethod
    def _input_shape_consistent(cls, args, shape=None):
        """
        >>> Array._input_shape_consistent([0])
        True
        >>> Array._input_shape_consistent([0, 0])
        True
        >>> Array._input_shape_consistent([[0, 0]])
        True
        >>> Array._input_shape_consistent([[0, 0], [0, 0]])
        True


        >>> Array._input_shape_consistent([[0, 0], [0]])
        False
        >>> Array._input_shape_consistent([[0, 0], [0, 0], [0, 0]])
        True
        >>> Array._input_shape_consistent([[0, 0], [0, 0], [[0, 0]]])
        False
        >>> Array._input_shape_consistent([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        True
        >>> Array._input_shape_consistent([[0, 0, 0], [0, 0], [0, 0]])
        False
        >>> Array._input_shape_consistent([[[0], 0, 0], [0, 0, 0], [0, 0, 0]])
        False
        >>> Array._input_shape_consistent([[[0, 0], 0, 0], [0, 0, 0], [0, 0, 0]])
        False

        # This cases needs to be addressed
        >>> Array._input_shape_consistent([[0, 0], [[0], 0]]) is False
        False

        """
        if shape is None:
            shape = cls._input_shape_extractor(args)
        if len(shape) == 1:
            return cls._has_len_or_none(args) == shape[0]
        else:
            return all(
                (cls._input_shape_consistent(arg, shape[1:]) for arg in args)
            )
        return False

    @classmethod
    def _flatten_structure(cls, args, shape=None):
        """
        >>> tuple(Array._flatten_structure((range(3), range(3, 6))))
        (0, 1, 2, 3, 4, 5)
        """
        if shape is None:
            shape = cls._input_shape_extractor(args)

        if len(shape) == 1:
            yield from args
            return

        for arg in args:
            yield from cls._flatten_structure(arg, shape[1:])

    def __add__(self, other):
        if isinstance(other, self.__class__) and self.shape == other.shape:
            return self.__class__(
                [a + b for (a, b) in zip(self._array, other._array)],
                shape=self.shape,
                flat_input=True,
            )

    def __sub__(self, other):
        if isinstance(other, self.__class__) and self.shape == other.shape:
            return self.__class__(
                [a - b for (a, b) in zip(self._array, other._array)],
                shape=self.shape,
                flat_input=True,
            )

    def __mul__(self, other):
        if self.__class__._type.is_compatible(other):
            return self.__class__(
                [a * other for a in self._array],
                shape=self.shape,
                flat_input=True,
            )

    def __truediv__(self, other):
        if self.__class__._type.is_compatible(other):
            return self.__class__(
                [a / other for a in self._array],
                shape=self.shape,
                flat_input=True,
            )

    def __eq__(self, other):
        """
        >>> B = Array(range(3), range(3, 6), range(6, 9))
        >>> B[2, :] == Array(6, 7, 8)
        True
        >>> B[:, 2] == Array(2, 5, 8)
        True
        >>> B[:, :] == B
        True
        """
        return (
            isinstance(other, self.__class__)
            and self.shape == other.shape
            and all(a == b for a, b in zip(self._array, other._array))
        )

    def __iter__(self):
        """
        This method will allow iteration, by yielding every element in the
        internal array, regardless of shape.

        >>> A = Array(1, 2, 3)
        >>> A._array == tuple(iter(A))
        True
        >>> B = Array([[1], [2], [3]])
        >>> B._array == tuple(iter(B))
        True
        """

        def _iterator():
            yield from self._array

        return _iterator()

    def __hash__(self):
        """Hash method:

        >>> A = Array(1, 2, 3)
        >>> A.__class__.__name__
        'Array'
        >>> hash(A) == hash(("Array", (3,), 1, 2, 3))
        True

        """
        return hash((self.__class__.__name__, self.shape, *self._array))
