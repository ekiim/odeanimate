from math import e
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes
from odeanimate.methods.polinomial import Polinomial, Curve1D


if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 12))
    interval = Interval(-10, 10)
    rows, cols = 3, 2
    axes = [
        cartesian_axes(fig.add_subplot(rows, cols, i + 1), interval)
        for i in range(rows * cols)
    ]
    functions = [
        f := Polinomial(-1, 0, 1),
        g := Polinomial(-1, 3, -3, 1),
        f + g,
        f + 2,
        h := Curve1D(function=lambda x: -0.2 * e**x),
        f + h,
    ]
    for func, ax in zip(functions, axes):
        ax.plot(list(interval), list(map(func, interval)))
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
