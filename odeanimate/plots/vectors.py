import math
from odeanimate.vector import Vector2D, Vector3D


def vector_2d_single(ax, vector, base=Vector2D(0, 0), label=None, **kwargs):
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
        **kwargs
    )
    if isinstance(label, str):
        angle = vector.angle
        # normal = vector.i / abs(vector)
        pos = base + vector / 2
        props = {"ha": "center", "va": "top"}
        ax.text(
            pos.x,
            pos.y,
            label,
            props,
            rotation=angle * (180 / math.pi),
            rotation_mode="anchor",
            transform_rotates_text=True,
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

def vector_3d_single(ax, vector, base=Vector3D(0, 0, 0), label=None, **kwargs):
    vector = Vector3D.from_vector(vector)
    base = Vector3D.from_vector(base)
    ax.quiver(
        [base.x], [base.y], [base.z],
        [vector.x], [vector.y], [vector.z],
    )
    return ax
