import pytest
from odeanimate.vector import Vector, Vector2D, Vector3D


class TestVectorFromMethods:
    @pytest.mark.parametrize(
        ["baseclass", "args"],
        (
            # Generic
            (Vector, (1, 2, 3)),
            (Vector, ((1, 2, 3),)),
            (Vector, Vector(1, 2, 3)),
            (Vector, (Vector(1, 2, 3),)),
            (Vector, ((Vector(1, 2, 3),),)),
            (Vector, Vector3D(1, 2, 3)),
            (Vector, (Vector3D(1, 2, 3),)),
            (Vector, ((Vector3D(1, 2, 3),),)),
            (Vector, Vector2D(2, 3)),
            (Vector, (Vector2D(2, 3),)),
            (Vector, ((Vector2D(2, 3),),)),
            # Vector 2D
            (Vector2D, (2, 3)),
            (Vector2D, ((2, 3),)),
            # (Vector2D, Vector(2,3)),
            (Vector2D, (Vector(2, 3),)),
            (Vector2D, ((Vector(2, 3),),)),
            (Vector2D, Vector2D(2, 3)),
            (Vector2D, (Vector2D(2, 3),)),
            (Vector2D, ((Vector2D(2, 3),),)),
            # Vector3D
            (Vector3D, (1, 2, 3)),
            (Vector3D, ((1, 2, 3),)),
            (Vector3D, Vector(1, 2, 3)),
            (Vector3D, (Vector(1, 2, 3),)),
            (Vector3D, ((Vector(1, 2, 3),),)),
            (Vector3D, Vector3D(1, 2, 3)),
            (Vector3D, (Vector3D(1, 2, 3),)),
            (Vector3D, ((Vector3D(1, 2, 3),),)),
        ),
    )
    def test_initialize_generic(self, baseclass, args):
        print(args)
        v = baseclass.from_compatible(*args)
        assert isinstance(v, baseclass)
