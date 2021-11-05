import matplotlib.pyplot as plt
from odeanimate.domains import Interval
from odeanimate.curve import Curve1D
from odeanimate.plots.axes import cartesian_axes
from odeanimate.plots.integrals import riemann_sum
from examples.output import output_file


@Curve1D
def f(x):
    return (1/3)*(x - 3.5)*x*(x-5)


if __name__ == '__main__':
    fig = plt.figure(figsize=(8, 8))
    integral_limits = Interval(1, 3)
    domain = Interval(0, 5)
    ax = cartesian_axes(
        fig.add_subplot(),
        x_min=domain.limits[0],
        x_max=domain.limits[1],
        y_max=(4/3)*max(map(f, domain)),
    )
    ax = riemann_sum(
        ax,
        f,
        integral_limits,
        5,
        domain=domain,
    )
    image_file = output_file(__file__, '.png')
    fig.savefig(image_file)
