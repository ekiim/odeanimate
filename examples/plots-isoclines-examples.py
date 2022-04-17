from math import sqrt, e
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.ode import plot_isocline
from odeanimate.plots.axes import cartesian_axes
from odeanimate.vector import Vector
from odeanimate.methods.ode import integrate, runge_kutta_4

import matplotlib.pyplot as plt

plt.rcParams["text.usetex"] = True


def tex_wrap(text):
    return f"${text}$"


@Vector.codomain
def frac(x, y):
    r"""$y^\prime = \frac{x}{y}$"""
    try:
        return (x / y,)
    except ZeroDivisionError:
        return (1e5,)


@Vector.codomain
def spiral(x, y):
    r"""$y^\prime = \frac{y-x}{y+ax}$"""
    try:
        return ((y - x) / (y + x),)
    except ZeroDivisionError:
        return (1e5,)


@Vector.codomain
def generic(x, y):
    r"""$y^\prime = \frac{e^{\frac{x}{2}}}{10} + \frac{xy}{3} - x$"""
    return ((1 / 10) * e ** (x / 2) + (1 / 3) * y * x - x,)


@Vector.codomain
def second(x, y):
    r"""$y^\prime = xy + y^2$"""
    return ((x * y + y**2),)


cases = [
    # (func, square, step)
    (frac, (-5, 5), 0.5),
    (spiral, (-8, 8), 1.0),
    (generic, (-5, 5), 0.5),
    (second, (-5, 5), 0.5),
]


def isocline_generator(func, square, step, name=None):
    if name is None:
        name = func.__name__
    fig = plt.figure(figsize=(8, 8))
    x_step, y_step = step, step
    x_interval, y_interval = Interval(*square), Interval(*square)
    ax = cartesian_axes(
        fig.add_subplot(),
        x_interval.limits[1] + x_step,
        y_interval.limits[1] + y_step,
        x_interval.limits[0] - x_step,
        y_interval.limits[0] - y_step,
    )
    ax = plot_isocline(ax, func, x_interval, y_interval, x_step, y_step, alpha=0.1)
    ax.text(
        0,
        1.5 * step + x_interval.limits[-1],
        "$y$",
        color="black",
        fontsize=18,
        horizontalalignment="center",
        verticalalignment="center",
    )
    ax.text(
        x_interval.limits[-1] + 1.5 * step,
        0,
        "$x$",
        color="black",
        fontsize=18,
        horizontalalignment="center",
        verticalalignment="center",
    )
    ax.text(
        x_interval.limits[0],
        x_interval.limits[-1],
        func.__doc__,
        color="black",
        fontsize=24,
        horizontalalignment="center",
        verticalalignment="center",
        bbox=dict(boxstyle="square", fc="white", ec="black", pad=0.2),
    )
    image_file = output_file(__file__, f"-{name}.png")
    print(image_file)
    fig.savefig(
        image_file,
        dpi=300,
    )


if __name__ == "__main__":
    for case in cases:
        print(case[0].__name__)
        isocline_generator(*case)
