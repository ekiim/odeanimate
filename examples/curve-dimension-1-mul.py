from math import e, cos, pi
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes
from odeanimate.curve import Curve1D


if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 12))
    interval = Interval(0, 10)
    interval_y = Interval(-3, 3)
    b, w = 1/3, 3*pi
    functions = [
        f := Curve1D(function=lambda x: e**(-b*x)),
        g := Curve1D(function=lambda x: cos(w*x)),
        f * g,
        g * 2,
        f*2,
        f*g*2
    ]
    rows = 3
    cols = 2
    axes = [
        cartesian_axes(
            fig.add_subplot(rows, cols, i+1),
            interval,
            interval_y
        )
        for i in range(rows*cols)
    ]
    for func, ax in zip(functions, axes):
        ax.plot(list(interval), list(map(func, interval)))
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
    


