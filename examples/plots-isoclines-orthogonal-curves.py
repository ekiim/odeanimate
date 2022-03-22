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
def parabolas_edo(x, y):
    r"""$y^\prime = 2\frac{y}{x}$"""
    try:
        return 2*y/x,
    except ZeroDivisionError:
        return 9e99,

@Vector.codomain
def elipses_edo(x, y):
    r"""$y^\prime = -\frac12\frac{x}{y}$"""
    try:
        return -x/(2*y),
    except ZeroDivisionError:
        return 9e99,

@Vector.codomain
def elipses(x, c=1):
    """$y = \\sqrt{\\frac{{c} - x^2}{2}}$"""
    if x**2 < c:
        return ((c - x**2)/2)**(1/2),
    else:
        return 0,

@Vector.codomain
def parabolas(x, c=1):
    """$y = {c} x^2$"""
    return c*x**2,

cases = [
    (parabolas_edo, (-5, 5), 0.5, (-5, 5), -10, 0.01, parabolas, "parabolas"),
    (parabolas_edo, (-5, 5), 0.5, (-5, 5), -10, 0.01, elipses, "parabolas-elipses"),
    (elipses_edo, (-5, 5), 0.5, (-5, 5), -10, 0.01, elipses, "elipses"),
    (elipses_edo, (-5, 5), 0.5, (-5, 5), -10, 0.01, parabolas, "elipses-parabolas"),
]


def isocline_generator(func, square, istep, interval, init, step, sol, name=None):
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
    c = 1
    int_domain = list(integration_interval(step))
    for c in [1/2, 1, 2, 5, 10, 20]:
        ax.plot(
            int_domain,
            [sol(x, c) for x in integration_interval(step)],
            linewidth=1,
            label=(sol.__doc__.replace("{c}", str(c)))
        )
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
    ax.legend(loc="lower right")
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

