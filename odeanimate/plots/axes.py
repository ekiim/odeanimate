from itertools import chain
import matplotlib.ticker as ticker
from odeanimate.domains import Interval


def cartesian_axes(ax, x_max, y_max=None, x_min=0, y_min=0, symetric=False):
    """Cartesian Axes

    This function will recieve an `Axes` object, and it will set it's configuration
    to be similar to a cartesian axes as we usually see it in books.

    The following arguments are:

        x_max: number | Interval
        y_max: Optional[number | Interval]
        x_min: number = 0
        y_min: number = 0
        symetric: bool = False

    If x_max is an Interval, then it will set x_min to the lower limit of it.
    If y_max is an Interval, then it will set y_min to the lower limit of it.
    If y_max is None, then it will set symetric to True.
    If symetric is True, then it will set y_min, y_max as x_min, y_max.

    The spines will show at the closes position posible to it's zero, with in
    the interval's range.

    This function will return you the Axes object that you passed to it.

    """
    if isinstance(x_max, Interval):
        x_min, x_max = x_max.limits
    x_min, x_max = sorted([x_min, x_max])
    if y_max is None:
        symetric = True
    if symetric:
        y_min, y_max = x_min, x_max
    elif isinstance(y_max, Interval):
        y_min, y_max = y_max.limits
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.spines["top"].set_color("none")
    ax.spines["right"].set_color("none")
    if x_min <= 0 <= x_max:
        ax.spines["left"].set_position("zero")
    else:
        ax.spines["left"].set_position(("data", min([x_min, x_max], key=abs)))
    if y_min <= 0 <= y_max:
        ax.spines["bottom"].set_position("zero")
    else:
        ax.spines["bottom"].set_position(("data", min([y_min, y_max], key=abs)))
    return ax


def interval_axes(ax, interval, *args, title=None, **kwargs):
    ax.spines["top"].set_color("none")
    ax.spines["bottom"].set_position("zero")
    ax.spines["left"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines.right.set_color("none")
    ax.spines.left.set_color("none")
    ax.spines.top.set_color("none")
    ax.xaxis.set_ticks_position("bottom")
    ax.tick_params(which="major", width=1.00, length=5, labelsize=10)
    ax.tick_params(which="minor", width=0, length=0)

    _min = min((interval.non_disjoint_interval), key=lambda i: i.limits[0]).limits[0]
    _max = max((interval.non_disjoint_interval), key=lambda i: i.limits[1]).limits[1]
    positions = list(
        chain(*list(map(lambda i: i.limits, interval.non_disjoint_interval)))
    )
    ax.xaxis.set_major_locator(ticker.FixedLocator(positions))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(positions))
    for i in interval.non_disjoint_interval:
        ax.plot(i.limits, [0, 0], linewidth=4)
        ax.scatter(i.limits, [0, 0], linewidth=4)
    ax.set_xlim(_min - 1, _max + 1)
    ax.set_ylim(-0.5, 0.5)
    if not title:
        title = "\\cup".join(
            [str(list(i.limits)) for i in interval.non_disjoint_interval]
        )
    ax.text(0.0, 0.75, title, transform=ax.transAxes, fontsize=14, color="tab:blue")
    return ax
