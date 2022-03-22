from math import sqrt
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes
from odeanimate.curve import Curve1D


@Curve1D
def func(x):
    return -(1 / 25) * (x + 1) * (x + 3) * (x - 7)


if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 8))
    step = 0.2
    x_interval = Interval(-2, 6)
    ax = cartesian_axes(
        fig.add_subplot(),
        x_interval.limits[1] + step,
        5 + step,
        x_interval.limits[0] - step,
        -1 - step,
    )
    ax.plot([x for x in x_interval(step)], [func(x) for x in x_interval(step)])
    x_0 = 3.5
    y_0 = func(x_0)
    m = func.derivative()(x_0)
    b = y_0 - m * x_0
    ax.plot([x for x in x_interval(step)], [m * x + b for x in x_interval(step)])
    ax.scatter([x_0], [y_0])

    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
