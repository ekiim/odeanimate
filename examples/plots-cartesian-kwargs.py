from math import sin, cos
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes

r = 2.5
circ_func = lambda x: (r ** 2 - x ** 2) ** (1 / 2)
x_plot = list(Interval(-r, r))
y_plot = [circ_func(x) for x in x_plot]
x_points = [0, 1, 1, -1, -1, 2, 2, -2, -2]
y_points = [0, 1, -1, 1, -1, 2, -2, 2, -2]


if __name__ == "__main__":
    fig = plt.figure(figsize=(16, 16))
    axes = [fig.add_subplot(4, 4, i) for i in range(1, 17)]

    full, pos, neg = Interval(-3, 3), Interval(0, 6), Interval(-6, 0)
    pos_non_zero, neg_non_zero = Interval(1, 7), Interval(-7, -1)

    axes[0] = cartesian_axes(axes[0], full, full)
    axes[1] = cartesian_axes(axes[1], full, symetric=True)

    axes[2] = cartesian_axes(axes[2], 3)

    axes[3] = cartesian_axes(axes[3], -3)

    axes[4] = cartesian_axes(axes[4], pos, pos)
    axes[5] = cartesian_axes(axes[5], pos, neg)
    axes[6] = cartesian_axes(axes[6], neg, pos)
    axes[7] = cartesian_axes(axes[7], neg, neg)

    axes[8] = cartesian_axes(axes[8], full, pos)
    axes[9] = cartesian_axes(axes[9], full, neg)
    axes[10] = cartesian_axes(axes[10], pos, full)
    axes[11] = cartesian_axes(axes[11], neg, full)

    axes[12] = cartesian_axes(axes[12], full, pos_non_zero)
    axes[13] = cartesian_axes(axes[13], full, neg_non_zero)
    axes[14] = cartesian_axes(axes[14], pos_non_zero, full)
    axes[15] = cartesian_axes(axes[15], neg_non_zero, full)

    for ax in axes:
        ax.plot(x_plot, y_plot)
        ax.plot(x_plot, [-y for y in y_plot])
        ax.scatter(x_points, y_points, c="g")

    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
