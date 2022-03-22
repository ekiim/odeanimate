from math import pi, sin, cos
import sys
from array import array
from pathlib import Path
from itertools import chain, repeat, product
from functools import reduce, lru_cache
import operator

# Constant used as base deltas.
h = 0.001
tolreance = 0.000001
tolerance = tolreance


def mul(values):
    return reduce(operator.mul, values, 1)


def to_list(arg):
    if hasattr(arg, "__iter__"):
        return arg
    else:
        return [arg]


def slice_to_range(s, limit=None):
    step = s.step or 1
    start, stop = s.start or 0, s.stop or limit
    return range(start, stop, step)


def dense_range(start, end, step=1):
    cur = start
    while abs(end - cur) < tolreance:
        yield cur
        cur += step


def tolerance_or_zero(x):
    return 0 if abs(x) < tolreance else x


def nth_roots_of_unity(n=1):
    return tuple(
        complex(
            tolerance_or_zero(cos(2 * pi * k / n)),
            tolerance_or_zero(sin(2 * pi * k / n)),
        )
        for k in range(1, n + 1)
    )


def kronecker_delta(i, j):
    return 1 if i == j else 0


def levi_civita(*i):
    signs = [1 if j < k else -1 if j > k else 0 for j, k in zip(i, i[1:])]
    return 0 if 0 in signs else -1 if signs.count(-1) > 1 else 1


class DenseRange:
    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step
        self.current = start

    def clone(self):
        return self.__class__(self.start, self.end, self.step)

    def __iter__(self):
        return self.clone()

    def __next__(self):
        # if abs(self.end - self.current - self.step*1.5) < tolreance:
        if self.current - self.end > tolreance:
            # print(self.start, self.end, self.current, self.step)
            raise StopIteration
        returnable = self.current
        self.current += self.step
        return returnable


def output_file(
    file, ext, project_root=Path(__file__).parent.parent, doc=None, **kwargs
):
    assets_dir = project_root / "assets"
    assets_dir.mkdir(exist_ok=True)
    return str(assets_dir / (Path(file).stem + ext))


class Interpolator:
    def __init__(self):
        self.values = dict()

    def add(self, t, value):
        self.values[t] = value
        self.__call__.cache_clear()

    @lru_cache(1000)
    def __call__(self, t):
        if t in self.values.keys():
            return self.values[t]
        m, M = self.limits
        if t > M or t < m:
            raise Exception("Out of bound")

        lower = min(filter(lambda k: k < self.values.keys()), key=lambda k: abs(t - k))
        upper = min(filter(lambda k: k > self.values.keys()), key=lambda k: abs(t - k))
        return t * (self.values[upper] - self.values[lower]) / (upper - lower)

    @property
    def limits(self):
        return (
            min(self.values.keys()),
            max(self.values.keys()),
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
