from pprint import pprint
from math import sin, cos, pi
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.curve import Curve3D


@Curve3D
def helicoid(t):
    return 3 * cos(2 * pi * t), 2 * sin(2 * pi * t), 3 * t / 4


@Curve3D
def spheric_curve(t):
    return (
        3 * cos(2 * pi * t) * cos(2 * pi * t),
        2 * sin(2 * pi * t) * cos(2 * pi * t),
        5 * sin(2 * pi * t),
    )


if __name__ == "__main__":
    x_0, x_n = -2, 2
    step = 1 / 100
    interval = Interval(x_0, x_n)
    X, Y, Z = [], [], []
    for t in interval(step):
        x, y, z = spheric_curve(t)
        X.append(x)
        Y.append(y)
        Z.append(z)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection="3d")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-5, 5)
    ax.plot(X, Y, Z, c=(0.25, 1.00, 0.25))
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
