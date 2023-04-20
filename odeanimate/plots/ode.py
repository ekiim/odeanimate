from math import atan, sin, cos
from pprint import pprint


def angle_from_slope(m):
    return atan(m)


def plot_isocline(
    ax, func, x_interval, y_interval, x_step=0.5, y_step=0.5, **kwargs
):
    x_len_factor = x_interval.__len__()
    y_len_factor = y_interval.__len__()
    xv = [[x for x in x_interval(x_step)] for y in y_interval(y_step)]
    yv = [[y for x in x_interval(x_step)] for y in y_interval(y_step)]
    line_factor = 1 / 10
    x_comp = (
        lambda x, y: line_factor
        * x_len_factor
        * cos(angle_from_slope(func(x, y)))
    )
    y_comp = (
        lambda x, y: line_factor
        * x_len_factor
        * sin(angle_from_slope(func(x, y)))
    )
    u = [
        [
            x_comp(x, y) / ((x_comp(x, y) ** 2 + y_comp(x, y) ** 2) ** 0.5)
            for x in x_interval(x_step)
        ]
        for y in y_interval(y_step)
    ]
    v = [
        [
            y_comp(x, y) / ((x_comp(x, y) ** 2 + y_comp(x, y) ** 2) ** 0.5)
            for x in x_interval(x_step)
        ]
        for y in y_interval(y_step)
    ]
    quiver_kwargs = dict(
        headwidth=0,
        minlength=0,
        alpha=0.05,
    )
    quiver_kwargs = {**quiver_kwargs, **kwargs}
    for piv in ["tail", "mid", "tip"]:
        ax.quiver(xv, yv, u, v, pivot=piv, **quiver_kwargs)
    # ax.scatter(xv, yv, marker='.', color='black')
    return ax
