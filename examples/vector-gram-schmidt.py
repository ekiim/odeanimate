import matplotlib.pyplot as plt
from odeanimate.vector import Vector


def Gram(*non):
    orth = []
    for (i, cur) in enumerate(non, start=0):
        x = cur - sum([
            ((cur @ other) / abs(other)**2)*other
            for other in orth[:i]
        ], start=Vector(0, 0, 0))
        orth.append(x)
    return orth


if __name__ == '__main__':
    non_ortho_base = [Vector(1, -1, 1), Vector(1, 0, 1), Vector(1, 1, 2)]
    ortho_base = Gram(*non_ortho_base)
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_zlim(0, 4)
    for (orig, ortho) in zip(non_ortho_base, ortho_base):
        ax.quiver(
            [0], [0], [0],
            [orig.values[0]], [orig.values[1]], [orig.values[2]],
            color='k',
            label='Original Base'
        )
        ax.quiver(
            [0], [0], [0],
            [ortho.values[0]], [ortho.values[1]], [ortho.values[2]],
            color='r',
            label='Orthonormal Base'
        )
    ax.view_init(10, 40)
