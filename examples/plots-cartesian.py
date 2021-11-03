from math import cos, pi
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.curve import Curve1D
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes

def wave(period=2*pi, theta=0, amplitude=1.5):
    @Curve1D
    def _wave(t):
        return amplitude*cos(2*pi*t/period + theta)
    return _wave


if __name__ == '__main__':
    fig = plt.figure(figsize=(8, 8))
    ax = cartesian_axes(
        fig.add_subplot(),
        10, 5, y_min=-5
    )
    interval = Interval(0, 10)
    f = wave(period=8*pi/5)
    f_dot = f.derivative()
    f_dot_dot = f_dot.derivative()
    ax.plot(
        list(interval),
        list(map(f, interval))
    )
    # ax.plot(interval, [f_dot(t) for t in interval])
    # ax.plot(list(interval), [f_dot_dot(t) for t in interval])
    image_file = output_file(__file__, '.png')
    fig.savefig(image_file)
