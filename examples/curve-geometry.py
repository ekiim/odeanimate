from math import sin, cos, pi
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.curve import Curve3D
from odeanimate.plots.vectors import vector_3d_single
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes

@Curve3D
def func(t):
    return (
        3 * cos(2 * pi * t) * cos(2 * pi * t),
        2 * sin(2 * pi * t) * cos(2 * pi * t),
        4 * sin(2 * pi * t),
    )

if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 8))
    rows, cols = 1, 1
    ax3d = fig.add_subplot(rows, cols, 1, projection="3d")

    interval, h = Interval(-4, 4), 1e-2

    trayectory = func.map(interval, h)
    T = trayectory[:,0]
    cords = [trayectory[:,1], trayectory[:,2], trayectory[:,3]]

    tangent = func.tangent()
    normal = func.normal()
    binormal = func.binormal()
    ax3d.plot(*cords, c=(0.25, 1.00, 0.25))
    t = 0.75
    print(func(t), tangent(t), normal(t), binormal(t), sep="\n")
    print(abs(tangent(t)), abs(normal(t)), abs(binormal(t)))
    vector_3d_single(ax3d, tangent(t), func(t))
    vector_3d_single(ax3d, normal(t), func(t))
    vector_3d_single(ax3d, binormal(t), func(t))


    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
    

