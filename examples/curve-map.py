from math import sin, cos, pi
import matplotlib.pyplot as plt
from odeanimate.utils import output_file
from odeanimate.curve import Curve3D
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes


@Curve3D
def spheric_curve(t):
    return (
        3 * cos(2 * pi * t) * cos(2 * pi * t),
        2 * sin(2 * pi * t) * cos(2 * pi * t),
        4 * sin(2 * pi * t),
    )


if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 8))
    rows, cols = 2, 2
    ax3d = fig.add_subplot(rows, cols, 1, projection="3d")

    interval, h = Interval(-4, 4), 1e-2
    func = spheric_curve
    axes = [
        cartesian_axes(fig.add_subplot(rows, cols, i + 1), Interval(-5, 5))
        for i in range(1, rows * cols)
    ]

    trayectory = spheric_curve.map(interval, h)
    T = trayectory[:, 0]
    cords = [trayectory[:, 1], trayectory[:, 2], trayectory[:, 3]]

    ax3d.plot(*cords, c=(0.25, 1.00, 0.25))
    for ax, cord in zip(axes, cords):
        ax.plot(T, cord)

    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
