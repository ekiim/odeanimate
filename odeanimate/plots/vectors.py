import math
from odeanimate.domains import Interval
from odeanimate.vector import Vector2D, Vector3D
from odeanimate.curve import Curve2D


def vector_2d_single(
    ax, vector, base=Vector2D(0, 0), label=None, no_rotate=False, **kwargs
):
    vector = Vector2D.from_vector(vector)
    base = Vector2D.from_vector(base)
    ax.quiver(
        [base.x],
        [base.y],
        [vector.x],
        [vector.y],
        angles="xy",
        scale_units="xy",
        scale=1,
        **kwargs,
    )
    if isinstance(label, str):
        angle = vector.angle_full
        # normal = vector.i / abs(vector)
        pos = base + vector / 2
        props = {"ha": "center", "va": "bottom"}
        ax.text(
            pos.x,
            pos.y,
            label,
            props,
            rotation=abs(angle * (180 / math.pi)),
            rotation_mode="anchor",
            transform_rotates_text=not no_rotate,
        )
    return ax


def vector_2d_tails(ax, *vectors, labels=None, **kwargs):
    initial = Vector2D(0, 0)
    for i, (prev, cur) in enumerate(zip([initial, *vectors], vectors)):
        initial += prev
        try:
            label = labels[i]
        except:
            label = None
        vector_2d_single(ax, cur, initial, label=label)
    return ax


def vector_2d_angle_between(ax, a, b, base=Vector2D(0, 0), label=None):
    A, B = (
        Vector2D.from_vector(a).angle_full,
        Vector2D.from_vector(b).angle_full,
    )

    if A > B:
        B = B + 2 * math.pi

    r = 0.3 * abs(min((a, b), key=lambda v: abs(v)))

    @Curve2D
    def _circle(t):
        _alpha = A + (B - A) * t
        return (
            r * math.cos(_alpha) + base.x,
            r * math.sin(_alpha) + base.y,
        )

    trajectory = (_circle + base).map(Interval(0, 1), 0.05)
    ax.plot(trajectory[:, 1], trajectory[:, 2])

    if isinstance(label, str):
        pos = _circle(0.5) * 1.5
        props = {"ha": "center", "va": "top"}
        ax.text(
            pos.x,
            pos.y,
            label,
            props,
        )
    return ax


def vector_3d_single(ax, vector, base=Vector3D(0, 0, 0), label=None, **kwargs):
    vector = Vector3D.from_vector(vector)
    base = Vector3D.from_vector(base)
    ax.quiver(
        [base.x],
        [base.y],
        [base.z],
        [vector.x],
        [vector.y],
        [vector.z],
    )
    return ax
