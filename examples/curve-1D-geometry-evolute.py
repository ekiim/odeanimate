from math import sin, cos, pi
import matplotlib.pyplot as plt
from odeanimate.utils import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes

# from odeanimate.plots.vectors import vector_2d_single
from odeanimate.curve import Curve2D
from odeanimate.methods.geometry import circle, line


@Curve2D
def cycloid(t):
    r = 0.5
    return (r * (t - sin(2 * pi * t)), r * (1 - cos(2 * pi * t)))


@Curve2D
def ellipse(t):
    a, b = 3, 1.5
    return a * cos(2 * pi * t), b * sin(2 * pi * t)


if __name__ == "__main__":
    fig = plt.figure(figsize=(12, 12))

    func = cycloid
    t_interval = Interval(0, 3)
    func = ellipse
    t_interval = Interval(0, 1)
    x_interval = Interval(-5, 5)
    step = 0.001
    rows, cols = 1, 1

    t = 0.1
    # t = t_interval.limits[0] + s*sum(t_interval.limits)

    # t = t_interval.limits[0] + s * sum(t_interval.limits)
    s = step

    ax = cartesian_axes(fig.add_subplot(rows, cols, 1), x_interval)
    trayectory = func.map(t_interval, step, keys=("t", "x", "y"))
    X, Y = trayectory[:, 1], trayectory[:, 2]
    ax.plot(X, Y)

    evolute = func.evolute()
    trayectory = evolute.map(t_interval, step, keys=("t", "x", "y"))
    X, Y = trayectory[:, 1], trayectory[:, 2]
    ax.plot(X, Y)

    # Plot current Circle
    center = evolute(t)
    circle = circle(center=center, r=1 / func.curvature()(t))
    trayectory = circle.map(Interval(0, 1), step, keys=("t", "x", "y"))
    X, Y = trayectory[:, 1], trayectory[:, 2]
    ax.plot(X, Y)

    trayectory = line(func(t), center).map(Interval(0, 1), step, keys=("t", "x", "y"))
    X, Y = trayectory[:, 1], trayectory[:, 2]
    ax.plot(X, Y)

    P, T, N, C = func(t), func.tangent()(t), func.normal()(t), center

    ax.scatter([P.x, C.x], [P.y, C.y], c="r")

    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
