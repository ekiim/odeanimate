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


@Vector.codomain
def frac(x, y):
    r"""\frac{x}{y}"""
    try:
        return (x / y,)
    except ZeroDivisionError:
        return (1e5,)


@Vector.codomain
def spiral(x, y):
    try:
        return ((y - x) / (y + x),)
    except ZeroDivisionError:
        return (1e5,)


@Vector.codomain
def generic(x, y):
    r"""$y^\prime = \frac{e^{\frac{x}{2}}}{10} + \frac{xy}{3} - x$"""
    return ((1 / 10) * e ** (x / 2) + (1 / 3) * y * x - x,)


cases = [
    # (func, square, mesh_int, interval, init, step)
    # (frac,    (-5, 5), 0.5, (-5,   5),  4.5, 0.5),
    # (spiral,  (-8, 2), 0.5, (-8, 1.5),    0, 0.25, "spiral-01"),
    # (generic, (-5, 5), 0.5, (-5,   5),  5.5, 0.5, "01"),
    # (generic, (-5, 5), 0.5, (-5,   5),  4.5, 0.5, "02"),
    # (generic, (-5, 5), 0.5, (-5,   5),  3.5, 0.5, "03"),
    # (generic, (-5, 5), 0.5, (-5,   5),  2.5, 0.5, "04"),
    # (generic, (-5, 5), 0.5, (-5,   5),  1.5, 0.5, "05"),
    # (generic, (-5, 5), 0.5, (-5,   5),  0.5, 0.5, "06"),
    # (generic, (-5, 5), 0.5, (-5,   5),  -0.5, 0.5, "07"),
    # (generic, (-5, 5), 0.5, (-5,   5),  -1.5, 0.5, "08"),
    (generic, (-5, 5), 0.5, (-5, 5), -2.5, 0.5, "09"),
    (generic, (-5, 5), 0.5, (-5, 5), -3.5, 0.5, "10"),
    (generic, (-5, 5), 0.5, (-5, 5), -3.5, 0.5, "11"),
    (generic, (-5, 5), 0.5, (-5, 5), -4.5, 0.5, "12"),
    (generic, (-5, 5), 0.5, (-5, 5), -5.5, 0.5, "13"),
    (generic, (-5, 5), 0.5, (-5, 5), -6.5, 0.5, "14"),
    (generic, (-5, 5), 0.5, (-4, 5), -10, 0.5, "20"),
]


def isocline_generator(func, square, istep, interval, init, step, name=None):
    if name is None:
        name = func.__name__
    fig = plt.figure(figsize=(8, 8))
    x_step, y_step, integral_step = istep, istep, step
    x_interval, y_interval = Interval(*square), Interval(*square)
    integration_interval = Interval(*interval)
    integration_initial_condition = init
    ax = cartesian_axes(
        fig.add_subplot(),
        x_interval.limits[1] + x_step,
        y_interval.limits[1] + y_step,
        x_interval.limits[0] - x_step,
        y_interval.limits[0] - y_step,
    )
    ax = plot_isocline(ax, func, x_interval, y_interval, x_step, y_step)
    y_integrated = list(
        integrate(
            runge_kutta_4,
            func,
            integral_step,
            *integration_interval.limits,
            integration_initial_condition,
        )
    )
    ax.plot(list(integration_interval(integral_step)), y_integrated)
    ax.scatter(integration_interval.limits, [y_integrated[0], y_integrated[-1]])
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
    ax.text(
        x_interval.limits[0],
        x_interval.limits[0],
        f"$({integration_interval.limits[0]},{integration_initial_condition})$",
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
