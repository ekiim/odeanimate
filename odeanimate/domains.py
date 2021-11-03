"""Domains

This file contains some classes that we can use to declare
domains for function evaluation.

The family of objects of type `MetaInterval`, should work
as _closed_ intervals and the user can use `|` for _union_
and `&` for _intersection_.

"""


from abc import ABC
from functools import reduce
from odeanimate.utils import h as _h, DenseRange


class MetaInterval(ABC):
    _parts = tuple()

    def __iter__(self):
        return self()

    def __hash__(self):
        return hash(("ODEInterval", *[i.limits for i in self._parts]))


class VoidInterval(MetaInterval):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return "<VoidInterval >"

    def __contains__(self, other):
        return isinstance(other, self.__class__)

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
        self.upper = b
        self.lower = a
        self._parts = [self]

    @property
    def limits(self):
        return (self.lower, self.upper)

    def __contains__(self, value):
        if isinstance(value, VoidInterval):
            return True
        if isinstance(value, Interval):
            return self.lower <= value.lower <= value.upper <= self.upper
        return self.lower <= value <= self.upper

    def __call__(self, h=_h):
        return DenseRange(self.lower, self.upper, h)

    def __repr__(self):
        return f"<Interval [{self.lower}, {self.upper}]>"

    def __len__(self):
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


class DisjointInterval(MetaInterval):
    def __init__(self, *intervals):
        self._parts = sorted(
            set(intervals),
            key=lambda k: k.limits[0]
        )

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

    def __rand__(self, other):
        return other & self

    def __ror__(self, other):
        return other | self

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
                lambda a, c:  c | a,
                map(lambda i: other & i, self._parts),
                VoidInterval()
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
        """
        if isinstance(other, VoidInterval):
            return self
        elif isinstance(other, Interval):
            memberships = list(filter(lambda i: i[1], enumerate((
                (other.limits[0] in i) or (other.limits[1] in i)
                for i in self._parts
            ))))
            ocurrence = len(memberships)
            if ocurrence == 2:
                first, last = [i[0] for i in memberships]
                A = self._parts[first] | other | self._parts[last]
                parts = [
                    *self._parts[:first], A, *self._parts[1+last:]
                ]
                return self.__class__(*parts) if len(parts) > 1 else A
            elif ocurrence == 1:
                index = memberships[0][0]
                interval = self._parts[index]
                A = interval | other
                if index == 0:
                    parts = [A, *self._parts[index + 1:] ]
                else:
                    parts = [*self._parts[:index], A]
                return self.__class__(*parts) if len(parts) > 1 else A
            elif ocurrence == 0:
                return self.__class__(*self._parts, other)
        elif isinstance(other, DisjointInterval):
            return reduce(lambda a, c: a | c, other._parts, self)
