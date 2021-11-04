from itertools import chain
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def cartesian_axes(ax, x_max, y_max, x_min=0, y_min=0, symetric=False):
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    return ax

def interval_axes(ax, interval, *args, title="Interval", **kwargs):
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines.right.set_color('none')
    ax.spines.left.set_color('none')
    ax.spines.top.set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(which='major', width=1.00, length=5, labelsize=10)
    ax.tick_params(which='minor', width=0, length=0)
    _min = min(
        (interval.non_disjoint_interval),
        key=lambda i: i.limits[0]
    ).limits[0]
    _max = max(
        (interval.non_disjoint_interval),
        key=lambda i: i.limits[1]
    ).limits[1]
    positions = list(
        chain(*list(map(
            lambda i: i.limits,
            interval.non_disjoint_interval
        )))
    )
    ax.xaxis.set_major_locator(
        ticker.FixedLocator(positions)
    )
    ax.xaxis.set_major_formatter(
        ticker.FixedFormatter(positions)
    )
    for i in interval.non_disjoint_interval:
        ax.plot(i.limits, [0,0], linewidth=4)
        ax.scatter(i.limits, [0,0], linewidth=4)
    ax.set_xlim(_min-1, _max+1)
    ax.set_ylim(-0.5, 0.5)
    ax.text(0.0, 0.2, title, transform=ax.transAxes,
            fontsize=14, fontname='Monospace', color='tab:blue')
    return ax
