from odeanimate.domains import Interval
from odeanimate.methods.integration import (
    riemann_variant,
    riemann_variant_step,
)
from odeanimate.plots.axes import cartesian_axes


def domain_fallback(interval):
    delta = len(interval) / 3
    return Interval(
        interval.limits[0] - delta,
        interval.limits[1] + 2 * delta,
    )


def riemann_sum(
    ax, f, interval, n, domain=None, variant="left", rectangle_color="g"
):
    domain = domain if domain else domain_fallback(interval)
    f_eval = list(map(f, domain))
    X, Y = list(domain), f_eval
    ax = cartesian_axes(
        ax,
        x_min=min(0, domain.limits[0]),
        x_max=max(0, domain.limits[1]),
        y_min=(5 / 4) * min(0, min(map(f, interval))),
        y_max=(5 / 4) * max(0, max(map(f, interval))),
    )
    step = len(interval) / n
    ax.plot(X, Y)
    area = 0
    for i, x in enumerate(interval(step)):
        eval_x = riemann_variant_step(variant, x, step)
        area += riemann_variant(variant, f, x, step)
        ax.plot(
            [x, x, x + step, x + step],
            [0, f(eval_x), f(eval_x), 0],
            c=rectangle_color,
        )
        ax.scatter([eval_x], [f(eval_x)], c=rectangle_color, s=100 / (n))

    for x in interval.limits:
        ax.plot(
            [x, x],
            [0, f(x)],
            linestyle="--",
            c="r",
            linewidth=2,
        )
    return ax, area


def riemann_integral(
    ax, f, interval, n, domain=None, rectangle_color="g", **kwargs
):
    return ax
