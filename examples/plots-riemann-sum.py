from math import exp, cos, sin, pi
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.curve import Curve1D
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes
from odeanimate.plots.integrals import riemann_sum, riemann_integral


@Curve1D
def f(x):
    r"""$\frac{1}{9}(x-\frac{7}{2})(x-\frac{6}{5})(x-2)+\frac{1}{2}$"""
    return (1 / 9) * (x - 3.5) * (x - 1.2) * (x - 2) + 0.5


@Curve1D
def g(x):
    r"""$e^{-\frac{x}{2}}\operatorname{cos}(2\pi x+\frac{1}{3})$"""
    return 5 * exp(-0.5 * x) * cos(2 * pi * x + 1 / 3)


@Curve1D
def h(x):
    r"""$\frac{sin(x)}{x}$"""
    return sin(x) / x


def riemann_sums_plot(f, interval, n, filenumber=None, name=""):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
    eq_axes = axes[0][0]
    rs_axes = [axes[0][1], axes[1][0], axes[1][1]]
    riemann_kwargs = dict(
        f=f,
        interval=interval,
        n=n,
    )
    fontsize = "18"
    eq_name = f.__doc__ if f.__doc__ else f.__name__
    eq_axes.text(0, 1, s="Riemann Sums", fontsize="20")
    eq_title = eq_axes.text(0, 0.8, s=eq_name, fontsize=fontsize)
    eq_axes.text(0, 0.5, s="interval:".capitalize(), fontsize=fontsize)
    eq_axes.text(
        0.5, 0.5, s="{}".format(interval.limits).capitalize(), fontsize=fontsize
    )
    eq_axes.text(0, 0.4, s="partition:".capitalize(), fontsize=fontsize)
    eq_axes.text(0.5, 0.4, s="{}".format(n), fontsize=fontsize)
    sum_text_start = 0.3
    eq_axes.get_xaxis().set_visible(False)
    eq_axes.get_yaxis().set_visible(False)
    for pos in ("bottom", "top", "right", "left"):
        eq_axes.spines[pos].set_color("none")
    for (i, ax, variant) in zip(range(3), rs_axes, ("mid", "left", "right")):
        ax, area = riemann_sum(ax, variant=variant, **riemann_kwargs)
        eq_axes.text(
            0,
            sum_text_start - i * 0.1,
            s="{}".format(variant).capitalize(),
            fontsize=fontsize,
        )
        eq_axes.text(
            0.5,
            sum_text_start - i * 0.1,
            s="{:02.5}".format(area).capitalize(),
            fontsize=fontsize,
        )
    image_file = output_file(
        __file__, "-{}-{:04}.png".format(name, filenumber if filenumber else n)
    )
    fig.savefig(image_file)


if __name__ == "__main__":
    cases = {
        # "polynomial": (f, Interval(1, 3)),
        # "sinx-over-x": (h, Interval(0.2, 3.2)),
        "dump-osc": (g, Interval(0, 5))
    }
    for name, case in cases.items():
        print(name)
        for i, n in enumerate([1, 2, 3, 5, 10, 20, 50, 100, 500, 1000]):
            riemann_sums_plot(*case, n, name=name, filenumber=i + 1)
            print(n, end=", ")
        else:
            print()
