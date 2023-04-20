from itertools import chain
from numbers import Number
import matplotlib.ticker as ticker
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from odeanimate.domains import Interval


class ODEAnimateAxes(Axes):
    name = "odeanimate"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x_min, x_max = -1, 1
        y_min, y_max = -1, 1
        self.spines["top"].set_color("none")
        self.spines["right"].set_color("none")
        self.set_xlim(x_min, x_max)
        self.set_ylim(y_min, y_max)
        self.set_xlabel("$x$", size=14, labelpad=-24, x=1.05)
        self.set_ylabel("$y$", size=14, labelpad=-21, y=1.05, rotation=0)

    def set_limits(self, x_interval, y_interval=None):
        if y_interval is None:
            y_interval = x_interval
        self.set_xlim(x_interval)
        self.set_ylim(y_interval)

    def set_xlim(self, x_min, x_max=None, *args, **kwargs):
        if isinstance(x_min, Interval):
            x_min, x_max = x_min.limits
        super().set_xlim(x_min, x_max)
        if x_min <= 0 <= x_max:
            self.spines["left"].set_position("zero")
        else:
            self.spines["left"].set_position(
                ("data", min([x_min, x_max], key=abs))
            )

    def set_ylim(self, y_min, y_max=None, *args, **kwargs):
        if isinstance(y_min, Interval):
            y_min, y_max = y_min.limits
        super().set_ylim(y_min, y_max)
        if y_min <= 0 <= y_max:
            self.spines["bottom"].set_position("zero")
        else:
            self.spines["bottom"].set_position(
                ("data", min([y_min, y_max], key=abs))
            )

    def add(self, *elements, **kwargs):
        for elem in elements:
            if hasattr(elem, "_plot_2d"):
                elem._plot_2d(self, **kwargs)
            elif isinstance(elem, (tuple, list)):
                self.add(*elem, **kwargs)
            elif elem is None:
                pass
            else:
                raise TypeError("Object does not support add plot.")
        return self

    def set_markers(self, x_markers=None, y_markers=None, major=True):
        for axis, markers in [(self.xaxis, x_markers), (self.yaxis, y_markers)]:
            if markers is not None and all(
                [isinstance(x, Number) for x in markers]
            ):
                markers = [(i, None) for i in markers]

            if markers is not None and all(
                [isinstance(x, tuple) for x in markers]
            ):
                makers = sorted(markers, key=lambda i: i[0])
                marks, labels = zip(*markers)
                getattr(
                    axis, "set_major_locator" if major else "set_minor_locator"
                )(ticker.FixedLocator(marks))
                if all([isinstance(label, str) for label in labels]):
                    getattr(
                        axis,
                        "set_major_formatter"
                        if major
                        else "set_minor_formatter",
                    )(ticker.FixedFormatter(labels))
                continue
            if markers is not None:
                raise Exception(
                    "Invalid marker structure, has to be list of numbers or list of tuples (X, label)"
                )


class ODEAnimateAxes3D(Axes3D):
    name = "odeanimate3D"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x_min, x_max = -1, 1
        y_min, y_max = -1, 1
        z_min, z_max = -1, 1
        self.set_xlim(x_min, x_max)
        self.set_ylim(y_min, y_max)
        self.set_zlim(z_min, z_max)

    def set_limits(self, x_interval, y_interval=None, z_interval=None):
        if y_interval is None:
            y_interval = x_interval
        if z_interval is None:
            z_interval = x_interval
        self.set_xlim(x_interval)
        self.set_ylim(y_interval)
        self.set_zlim(z_interval)

    def set_xlim(self, x_min, x_max=None, *args, **kwargs):
        if isinstance(x_min, Interval):
            x_min, x_max = x_min.limits
        super().set_xlim(x_min, x_max)

    def set_ylim(self, y_min, y_max=None, *args, **kwargs):
        if isinstance(y_min, Interval):
            y_min, y_max = y_min.limits
        super().set_ylim(y_min, y_max)

    def set_zlim(self, z_min, z_max=None, *args, **kwargs):
        if isinstance(z_min, Interval):
            z_min, z_max = z_min.limits
        super().set_zlim(z_min, z_max)

    def add(self, *elements, **kwargs):
        for elem in elements:
            if hasattr(elem, "_plot_3d"):
                elem._plot_3d(self, **kwargs)
            elif isinstance(elem, (tuple, list)):
                self.add(*elem, **kwargs)
            elif elem is None:
                pass
            else:
                raise TypeError("Object does not support add plot.")
        return self


def cartesian_axes(
    ax, x_max, y_max=None, x_min=0, y_min=0, symetric=False, labels=None
):
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

    if isinstance(labels, (list, tuple)) and len(labels) == 2:
        ax.text(
            (x_max - x_min) * 0.05,
            y_max + (y_max - y_min) * 0.2,
            labels[1],
            fontsize="12",
        )
        ax.text(
            x_max + (x_max - x_min) * 0.2,
            (y_max - y_min) * 0.05,
            labels[0],
            fontsize="12",
        )

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

    _min = min(
        (interval.non_disjoint_interval), key=lambda i: i.limits[0]
    ).limits[0]
    _max = max(
        (interval.non_disjoint_interval), key=lambda i: i.limits[1]
    ).limits[1]
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
    ax.text(
        0.0, 0.75, title, transform=ax.transAxes, fontsize=14, color="tab:blue"
    )
    return ax
