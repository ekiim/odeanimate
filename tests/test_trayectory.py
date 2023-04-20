from random import random
import pytest
from odeanimate.array import Array
from odeanimate.vector import Vector
from odeanimate.domains import Interval
from odeanimate.codomain import Trajectory


def random_vector(cls=Vector, n=4):
    return cls(*(random() for _ in range(n)))


class TestTrayectory:
    def test_trayectory_constructor(self):
        trajectory = Trajectory(*[random_vector() for _ in range(100)])

        assert isinstance(trajectory, Trajectory)

    def test_trayectory_constructor_with_keys(self):
        length = 100

        trajectory = Trajectory(
            *[random_vector(n=4) for _ in range(length)],
            keys=("t", "x", "y", "z"),
        )

        assert isinstance(trajectory, Trajectory)
        assert trajectory._keys == ("t", "x", "y", "z")

        trajectory_x = trajectory.x

        assert isinstance(trajectory_x, Array)
        assert len(trajectory_x) == length

        assert isinstance(trajectory["x"], Array)
        assert len(trajectory["x"]) == length

        assert (
            repr(trajectory)
            == "<Trajectory rows=100 cols=4 keys=('t', 'x', 'y', 'z')>"
        )
