import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import interval_axes

if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 3))
    ax = interval_axes(fig.add_subplot(), Interval(-1, 1) | Interval(2, 3))
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
