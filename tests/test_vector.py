import pytest
from odeanimate.array import Array
from odeanimate.constants import pi
from odeanimate.vector import Vector


class TestVectorGeneric:
    tolerance = 1e-7

    def test_initialize(self):
        v = Vector(1.0, 1.0)
        assert isinstance(v, Vector)
        assert v.dimension == 2
        assert isinstance(v, Array)

    def test_initialize_from_vector(self):
        v = Vector(1.0, 1.0)
        w = Vector(v)
        assert isinstance(w, Vector)
        assert v.dimension == 2
        assert isinstance(v, Array)

    def test_initialize_error(self):
        with pytest.raises(Exception):
            Vector(1, "1")

    def test_dimension(self):
        v = Vector(1.0, 1.0)
        assert v.dimension == len(v)
        assert v.dimension == 2

    def test_euclidean_euclidean_norm(self):
        v = Vector(3.0, 4.0)
        assert 5.0 == v.norm()

    def test_euclidean_norm_p_1(self):
        v = Vector(-3.0, 4.0)
        assert 7.0 == v.norm(p=1)

    def test_euclidean_norm_p_2(self):
        v = Vector(-3.0, 4.0)
        assert (
            len(
                {
                    v.euclidean_norm(),
                    v.norm(p=2),
                    abs(v),
                    5.0,
                }
            )
            == 1
        )

    @pytest.mark.parametrize(
        ["v", "w", "result"],
        [
            (Vector(1, -1), Vector(1, 1), 0),
            (Vector(2, -1), Vector(2, 1), 3),
        ],
    )
    def test_dot_product(self, v, w, result):
        dot_result = v.dot(w)
        mul_result = v * w
        assert dot_result == mul_result
        assert dot_result == result

    @pytest.mark.parametrize(
        ["v", "w", "result"],
        [
            (Vector(1, -1), 2, Vector(2, -2)),
            (Vector(2, -1), Vector(2, 1), 3),
        ],
    )
    def test_mul(self, v, w, result):
        assert result == v * w
        assert result == w * v

    @pytest.mark.parametrize(
        ["v", "w", "result"],
        [
            (Vector(1, -1), Vector(1, 1), Vector(2, 0)),
            (Vector(2, -1), Vector(2, 1), Vector(4, 0)),
        ],
    )
    def test_add(self, v, w, result):
        assert v + w == result
        assert w + v == result

    @pytest.mark.parametrize(
        ["v", "w", "result"],
        [
            (Vector(1, -1), 1, Vector(1, -1)),
            (Vector(2, -4), -2, Vector(-1, 2)),
        ],
    )
    def test_truediv(self, v, w, result):
        assert (v / w) == result

    @pytest.mark.parametrize(
        ["v", "w"],
        [
            (Vector(1, -1), Vector(1, -1)),
            (-2, Vector(2, -4)),
        ],
    )
    def test_truediv_error(self, v, w):
        with pytest.raises(TypeError):
            v / w

    @pytest.mark.parametrize(
        ["v", "w", "result"],
        [
            (Vector(1, -1), Vector(1.0, -1.0), True),
            (Vector(1, 1), Vector(1.0, -1.0), False),
            (Vector(1, 1), Vector(1.0, -1.0, 0), False),
        ],
    )
    def test_equal(self, v, w, result):
        assert (v == w) == result

    def test_one_dimensional(self):
        v = Vector(2)
        assert isinstance(v, Vector)
        assert len(v) == 1
        assert float(v) == v[0]
        assert v / 2 == Vector(1)
        assert 2 / v == Vector(1)

    def test_direction_error(self):
        with pytest.raises(ZeroDivisionError):
            Vector(0).direction

    @pytest.mark.parametrize(
        ["v"],
        [
            (Vector(1, -1),),
            (Vector(2, -1, 2),),
        ],
    )
    def test_direction_magnitude(self, v):
        assert abs(abs(v.direction) - 1) < self.tolerance

    @pytest.mark.parametrize(
        ["v", "w", "result"],
        [
            (Vector(1, -1), Vector(1, -1), 0),
            (Vector(1, -1), Vector(-1, 1), pi),
        ],
    )
    def test_angle_between(self, v, w, result):
        assert abs(v.angle_with(w) - result) < self.tolerance

    @pytest.mark.parametrize(
        ["vector", "unit_vector"],
        [
            (Vector(1, -1), Vector(2 ** (-0.5), -(2 ** (-0.5)))),
        ],
    )
    def test_direction(self, vector, unit_vector):
        for x in vector.direction - unit_vector:
            assert abs(x) < self.tolerance
