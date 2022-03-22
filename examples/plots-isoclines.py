from math import sqrt, e
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.ode import plot_isocline
from odeanimate.plots.axes import cartesian_axes
from odeanimate.vector import Vector
from odeanimate.methods.ode import integrate, runge_kutta_4


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
    return ((1 / 10) * e ** (x / 2) + (1 / 3) * y * x - x,)


cases = [
    # (func, square, interval, init, step)
    (frac, (-5, 5), Interval(-5, 5), 4.5, 0.5),
    (spiral, (-5, 5), Interval(0.1, 5), 0.1, 0.5),
    (generic, (-5, 5), Interval(-5, 5), 4.5, 0.5),
]


if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 8))
    func = generic
    step = 1
    x_step, y_step = step, step
    x_interval = Interval(-3, 3)
    y_interval = Interval(-3, 3)
    ax = cartesian_axes(
        fig.add_subplot(),
        x_interval.limits[1] + x_step,
        y_interval.limits[1] + y_step,
        x_interval.limits[0] - x_step,
        y_interval.limits[0] - y_step,
    )
    integration_interval = x_interval
    integral_step = 0.2
    initial_condition_start = 2 / 3
    for initial_condition in range(5):
        y_integrated = list(
            integrate(
                runge_kutta_4,
                func,
                integral_step,
                *integration_interval.limits,
                initial_condition_start * (1 + initial_condition)
            )
        )
        ax = plot_isocline(ax, func, x_interval, y_interval, x_step, y_step)
        ax.plot(list(integration_interval(integral_step))[:-1], y_integrated)
        ax.scatter(integration_interval.limits, [y_integrated[0], y_integrated[-1]])

    image_file = output_file(__file__, ".png")
    fig.savefig(
        image_file,
        dpi=300,
    )
