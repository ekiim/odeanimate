import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes


def piecewise(x):
    if x in Interval(-1, 1):
        return x**2
    return abs(x)


if __name__ == "__main__":
    fig = plt.figure(figsize=(16, 16))
    step = 1 / 10
    x_int, y_int = Interval(-3, 3), Interval(-1, 5)
    axes = cartesian_axes(fig.add_subplot(), x_int, y_int)
    x_points = list(x_int(step))
    y_points = [piecewise(x) for x in x_int(step)]
    axes.plot(x_points, y_points)
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
