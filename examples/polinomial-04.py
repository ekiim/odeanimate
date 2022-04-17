import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes
from odeanimate.methods.polinomial import Polinomial


if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 8))
    interval = Interval(-10, 10)
    ax = cartesian_axes(fig.add_subplot(), interval)
    f = Polinomial(-1, 0, 1)
    ax.plot(list(interval), list(map(f, interval)))
    g = Polinomial(23, -2, 3, -1, 1)
    ax.plot(list(interval), list(map(g, interval)))
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
