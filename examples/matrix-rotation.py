from math import pi
import matplotlib.pyplot as plt
from odeanimate.utils import output_file
from odeanimate.domains import Interval
from odeanimate.vector import Vector2D
from odeanimate.matrix import Matrix
from odeanimate.plots.axes import cartesian_axes
from odeanimate.plots.vectors import vector_2d_tails, vector_2d_single

if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 8))
    interval = Interval(-5, 5)
    a = Vector2D(2, 2)
    b = Vector2D(2, -2)
    rows, cols = 3, 3
    functions = [
        Matrix([1, 0], [0, 1]),
        Matrix([2, 0], [0, 2]),
        Matrix([0.5, 0], [0, 0.5]),
        Matrix.Rotation2D(pi / 2),
        Matrix.Rotation2D(pi),
        Matrix.Rotation2D(3 * pi / 2),
        Matrix([0, -1], [-1, 1]),
        0.5 * Matrix([1, 1], [1, 2]),
        Matrix([0.5, 0], [0, 0.5]),
    ]
    axes = [
        cartesian_axes(fig.add_subplot(rows, cols, i + 1), interval)
        for i in range(rows * cols)
    ]
    for func, ax in zip(functions, axes):
        _a = func(a)
        vector_2d_single(ax, _a)
        vector_2d_single(ax, func(b), _a)
        pass
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
