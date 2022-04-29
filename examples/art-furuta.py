from math import cos, pi, sin

import matplotlib.pyplot as plt

from odeanimate.utils import output_file
from odeanimate.curve import Curve2D
from odeanimate.domains import Interval
from odeanimate.methods.geometry import line
from odeanimate.plots.axes import cartesian_axes
from odeanimate.plots.vectors import (
    vector_3d_single,
    vector_2d_single,
    vector_2d_angle_between,
)
from odeanimate.vector import Vector, Vector3D

plt.rcParams["text.usetex"] = False


def furuta_plot(l_1, l_2, theta, phi, view):
    height_z = 1.5 * l_2
    # Figure Configuration
    fig = plt.figure(figsize=(16, 8))
    gs = fig.add_gridspec(2, 4)
    ax3d = fig.add_subplot(gs[:, 0:-1], projection="3d")
    ax3d.set_xlim(-l_1, l_1)
    ax3d.set_ylim(-l_1, l_1)
    ax3d.set_zlim(0, 2 * height_z)
    ax3d.view_init(*view)
    ax3d.set_xlabel("$x$", fontsize=20)
    ax3d.set_ylabel("$y$", fontsize=20)
    ax3d.set_zlabel("$z$", fontsize=20)

    ax_z = cartesian_axes(
        fig.add_subplot(gs[0, -1]), Interval(-l_1, l_1), labels=["$x$", "$y$"]
    )
    ax_t = cartesian_axes(
        fig.add_subplot(gs[1, -1]), Interval(-l_2, l_2), labels=["$T$", "$z$"]
    )

    # Paramterization
    origin, z = Vector3D(0, 0, 0), Vector3D(0, 0, 1)
    pivot = height_z * z

    rod_1 = l_1 * Vector3D(cos(theta), sin(theta), 0)

    T = z ^ rod_1.direction

    rod_2 = l_2 * (cos(phi) * z + sin(phi) * T)

    # 3D Axes Plot
    rot_axis = line(origin, pivot).map(Interval(0, 1), keys=("t", "x", "y", "z"))
    ax3d.plot(rot_axis.x, rot_axis.y, rot_axis.z)
    vector_3d_single(ax3d, rod_1, pivot, label="$l_1$", no_rotate=True)
    vector_3d_single(ax3d, rod_2, rod_1 + pivot, label="$l_2$", no_rotate=True)

    # Y vs X Axes
    rod_1_yx = Vector(rod_1.x, rod_1.y)
    rod_2_yx = Vector(rod_2.x, rod_2.y)

    ax_z.set_xlim(-l_1 * (2**0.5), l_1 * (2**0.5))
    ax_z.set_ylim(-l_1 * (2**0.5), l_1 * (2**0.5))
    vector_2d_single(ax_z, rod_1_yx, label="$l_1$")
    vector_2d_angle_between(ax_z, Vector(l_1, 0), rod_1_yx, label=r"$\theta$")
    vector_2d_single(ax_z, rod_2_yx, rod_1_yx, label=r"$l_2\sin(\phi)$", no_rotate=True)

    # Z vs Tangent Axes
    ax_t.set_xlim(-l_2 * (2**0.5), l_2 * (2**0.5))
    ax_t.set_ylim(-l_2 * (2**0.5), l_2 * (2**0.5))
    rod_2_zT = Vector(rod_2 * T, rod_2 * z)
    vector_2d_single(ax_t, rod_2_zT, label="$l_2$")
    vector_2d_angle_between(ax_t, rod_2_zT, Vector(0, l_2), label=r"$\phi$")

    return fig


if __name__ == "__main__":
    L_1, L_2 = 3, 2
    _theta, _phi = 2 * pi * 0.4, 2 * pi * 0.4
    _view = (25, 45)
    fig = furuta_plot(L_1, L_2, _theta, _phi, _view)
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
