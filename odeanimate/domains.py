"""Domains

This file contains some classes that we can use to declare
domains for function evaluation.

The family of objects of type `MetaInterval`, should work
as _closed_ intervals and the user can use `|` for _union_
and `&` for _intersection_.

"""

import sys

from abc import ABC, abstractmethod
from functools import reduce
from odeanimate.utils import h as _h, DenseRange


class MetaInterval(ABC):
    _parts = tuple()

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    def __iter__(self):
        return self()

    def __hash__(self):
        return hash(("ODEInterval", *[i.limits for i in self._parts]))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __rand__(self, other):
        return other & self

    def __ror__(self, other):
        return other | self

    @property
    def non_disjoint_interval(self):
        return self._parts


class VoidInterval(MetaInterval):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return "<VoidInterval >"

    def __contains__(self, other):
        """
        >>> 1 in VoidInterval()
        False
        >>> VoidInterval() in VoidInterval()
        True
        """
        return isinstance(other, self.__class__)

    def __bool__(self):
        return False

    def __len__(self):
        return 0

    def __or__(self, other):
        """
        >>> VoidInterval() | Interval(0, 1)
        <Interval [0, 1]>
        >>> Interval(0, 1) | VoidInterval()
        <Interval [0, 1]>
        """
        if isinstance(other, MetaInterval):
            return other
        raise Exception("Can not do union")

    def __and__(self, other):
        """
        >>> VoidInterval() & Interval(0, 1)
        <VoidInterval >
        >>> Interval(0, 1) & VoidInterval()
        <VoidInterval >
        """
        if isinstance(other, MetaInterval):
            return self
        raise Exception("Can not do intersection")


class Interval(MetaInterval):
    def __init__(self, a, b):
        if a > b:
            raise Exception("Invalid values for an interval")
        self.upper, self.lower = b, a
        self._parts = [self]

    @property
    def limits(self):
        return (self.lower, self.upper)

    def __contains__(self, value):
        """
        >>> VoidInterval() in Interval(0, 1)
        True
        >>> VoidInterval() not in Interval(0, 1)
        False
        >>> 1.5 in Interval(1, 2)
        True
        >>> 1 in Interval(1, 2)
        True
        >>> 2 in Interval(1, 2)
        True
        >>> 0 in Interval(1, 2)
        False
        >>> 3 in Interval(1, 2)
        False
        >>> Interval(1,2) in Interval(0, 2)
        True
        >>> Interval(0,2) in Interval(1, 2)
        False
        >>> Interval(1,2) in Interval(1, 2)
        True
        """
        if isinstance(value, VoidInterval):
            return True
        if isinstance(value, Interval):
            return self.lower <= value.lower <= value.upper <= self.upper
        return self.lower <= value <= self.upper

    def __call__(self, h=_h, func=None):
        returnable = DenseRange(self.lower, self.upper, h)
        if callable(func):
            returnable.apply(func)
        return returnable

    def __repr__(self):
        return f"<Interval [{self.lower}, {self.upper}]>"

    def __len__(self):
        """
        >>> len(Interval(0, 1))
        1
        >>> len(Interval(0, 2))
        2
        >>> len(Interval(-1, 2))
        3
        """
        return self.upper - self.lower

    def __or__(self, other):
        """
        >>> Interval(1, 2) | Interval(2, 3)
        <Interval [1, 3]>
        >>> Interval(1, 2) | Interval(1.5, 1.75)
        <Interval [1, 2]>
        >>> Interval(1, 2) | Interval(1, 2)
        <Interval [1, 2]>
        >>> Interval(1.5, 1.75) | Interval(1, 2)
        <Interval [1, 2]>
        >>> Interval(1, 1.5) | Interval(2, 3)
        <DisjointInterval [1, 1.5]U[2, 3]>
        >>> Interval(2, 3) | Interval(1, 1.5)
        <DisjointInterval [1, 1.5]U[2, 3]>
        >>> Interval(2, 3) | Interval(1, 1.5)
        <DisjointInterval [1, 1.5]U[2, 3]>
        """
        if not isinstance(other, MetaInterval):
            raise NotImplementedError
        if isinstance(other, VoidInterval):
            return self
        a, b = self.limits
        c, d = other.limits
        if c in self:
            return Interval(a, max(b, d))
        if b in other:
            return Interval(min(a, c), d)
        return DisjointInterval(self, other)

    def __and__(self, other):
        """
        >>> Interval(1, 2) & Interval(1, 1.5)
        <Interval [1, 1.5]>
        >>> Interval(1, 2) & Interval(-1, 2)
        <Interval [1, 2]>
        >>> Interval(1, 2) & Interval(2, 3)
        <Interval [2, 2]>
        >>> Interval(1, 2) & Interval(2.5, 3)
        <VoidInterval >
        >>> Interval(1, 2.5) & Interval(2, 2.5)
        <Interval [2, 2.5]>
        """
        if not isinstance(other, MetaInterval):
            raise NotImplementedError
        if isinstance(other, VoidInterval):
            return VoidInterval()
        if isinstance(other, Interval):
            a, b = self.limits
            c, d = other.limits
            if (c in self) or (b in other) or (a in other) or (d in self):
                return Interval(max(a, c), min(b, d))
            else:
                return VoidInterval()
        raise NotImplementedError

    def _repr_latex_(self):
        return f"${self.limits}$"


class DisjointInterval(MetaInterval):
    @staticmethod
    def assist(acc, cur):
        last = acc[-1]
        # print(acc, last, cur, file=sys.stderr)
        # print(type(last), type(cur), file=sys.stderr)
        tmp = last & cur
        # print(tmp, tmp == VoidInterval(), file=sys.stderr)
        if tmp in VoidInterval():
            return [*acc, cur]
        if isinstance(tmp, Interval):
            return [*acc[:-1], last | cur]
        return [VoidInterval()]

    def __init__(self, *intervals):
        """
        >>> DisjointInterval(Interval(1, 2), Interval(2, 3), Interval(3, 4))
        <Interval [1, 4]>
        """
        # print("Pre:\t", self._parts, file=sys.stderr)
        self._parts = reduce(
            self.assist,
            sorted(set(intervals), key=lambda k: k.limits),
            [VoidInterval()],
        )[1:]
        # print("Post:\t", self._parts, file=sys.stderr)
        if len(self._parts) == 1:
            self._cast_to_interval()

    def _cast_to_interval(self):
        self.__class__ = Interval
        self.lower, self.upper = self._parts[0].limits

    def __repr__(self):
        label = "U".join([str(list(i.limits)) for i in self._parts])
        return f"<DisjointInterval {label}>"

    def __contains__(self, other):
        """
        >>> 1.5 in (Interval(1, 2) | Interval(3, 4))
        True
        >>> 2.5 in (Interval(1, 2) | Interval(3, 4))
        False
        """
        return any((other in i for i in self._parts))

    def __len__(self):
        return sum(map(len, self._parts))

    def __and__(self, other):
        """
        >>> Interval(1, 2) & Interval(3, 4)
        <VoidInterval >
        >>> Interval(1, 2) & Interval(2, 2.5)
        <Interval [2, 2]>
        >>> Interval(1, 2) | Interval(3, 4) | Interval(2, 2.5) | Interval(2.5, 3)
        <Interval [1, 4]>
        >>> (Interval(1, 2.5) | Interval(3, 4)) & Interval(2, 3.5)
        <DisjointInterval [2, 2.5]U[3, 3.5]>
        """
        if isinstance(other, VoidInterval):
            return VoidInterval()
        elif isinstance(other, Interval):
            return reduce(
                lambda a, c: c | a,
                map(lambda i: other & i, self._parts),
                VoidInterval(),
            )
        elif isinstance(other, DisjointInterval):
            return reduce(lambda a, c: a & c, other._parts, self)

    def __or__(self, other):
        """
        >>> Interval(1, 2) | Interval(3, 4) | Interval(2, 3)
        <Interval [1, 4]>
        >>> Interval(1, 2) | Interval(3, 4) | Interval(2, 2.5)
        <DisjointInterval [1, 2.5]U[3, 4]>
        >>> Interval(1, 2) | Interval(3, 4) | Interval(2, 2.5) | Interval(2.5, 3)
        <Interval [1, 4]>
        >>> Interval(1, 2) | Interval(3, 4) | Interval(2, 2.5) | Interval(5, 6)
        <DisjointInterval [1, 2.5]U[3, 4]U[5, 6]>
        >>> (Interval(1, 2) | Interval(3, 4)) | (Interval(2, 2.5) | Interval(5, 6))
        <DisjointInterval [1, 2.5]U[3, 4]U[5, 6]>
        >>> (Interval(1, 2) | Interval(3, 4) | Interval(2, 2.5) | Interval(1, 6))
        <Interval [1, 6]>
        """
        if isinstance(other, VoidInterval):
            return self
        elif isinstance(other, (Interval, DisjointInterval)):
            return DisjointInterval(*other._parts, *self._parts)


class Mesh:
    def __init__(self, *args, **kwargs):
        pass


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
