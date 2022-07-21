from math import cos, pi, sin
import matplotlib.pyplot as plt
from odeanimate.utils import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes
from odeanimate.plots.vectors import (
    vector_2d_single,
    vector_2d_angle_between,
)
from odeanimate.vector import Vector2D

if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 8))

    v = Vector2D(1, 0.5).direction * 2
    w = Vector2D(1, 1)
    u = Vector2D(-1, 1)

    ax = cartesian_axes(fig.add_subplot(2, 2, 1), Interval(-2, 2))
    vector_2d_single(ax, v)
    vector_2d_single(ax, w)
    vector_2d_angle_between(ax, v, w, label="A")

    ax = cartesian_axes(fig.add_subplot(2, 2, 2), Interval(-2, 2))
    vector_2d_single(ax, v)
    vector_2d_single(ax, u)
    vector_2d_angle_between(ax, v, u, label="A")

    ax = cartesian_axes(fig.add_subplot(2, 2, 3), Interval(-2, 2))
    vector_2d_single(ax, v)
    vector_2d_single(ax, w)
    vector_2d_angle_between(ax, w, v, label="B")

    ax = cartesian_axes(fig.add_subplot(2, 2, 4), Interval(-2, 2))
    vector_2d_single(ax, v)
    vector_2d_single(ax, u)
    vector_2d_angle_between(ax, u, v, label="A")

    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
