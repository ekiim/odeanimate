from math import e
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes
from odeanimate.methods.polinomial import Polinomial, Curve1D


if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 12))
    interval = Interval(-10, 10)
    functions = [
        f := Polinomial(-1, 0, 1),
        g := Polinomial(-1, 3, -3, 1),
        f * 2,
        f * g,
        h := Curve1D(function=lambda x: -0.2*e**x),
        f * h
    ]
    rows, cols = 3, 2
    axes = [
        cartesian_axes(fig.add_subplot(rows, cols, i+1), interval)
        for i in range(rows*cols)
    ]
    for func, ax in zip(functions, axes):
        if isinstance(func, Polinomial):
            print(func)
        else:
            print("Not a polinomial")
        ax.plot(list(interval), list(map(func, interval)))
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)

