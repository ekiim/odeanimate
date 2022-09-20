import pytest
from odeanimate.curve import (
    Curve,
    Curve1D,
    Curve2D,
    Curve3D,
)
from odeanimate.domains import Interval
from odeanimate.codomain import Trajectory


class TestCurveMapping:
    def test_curve_basic(self):
        @Curve
        def function(t):
            return t, t, t

        interval = Interval(-1, 1)
        delta = 0.1

        trayectory = function.map(interval, delta)

        assert isinstance(trayectory, Trajectory)

        assert isinstance(abs(function), Curve1D)
        assert isinstance(function * function, Curve1D)
