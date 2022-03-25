import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.vector import Vector


def GramSchmidtOrthoNormalize(*non):
    orth = []
    for (i, cur) in enumerate(non, start=0):
        x = cur - sum(
            [((cur * other) / abs(other) ** 2) * other for other in orth[:i]],
            start=Vector(0, 0, 0),
        )
        orth.append(x / abs(x))
    return orth


if __name__ == "__main__":
    non_ortho_base = [Vector(1, -1, 1), Vector(1, 0, 1), Vector(1, 1, 2)]
    ortho_base = GramSchmidtOrthoNormalize(*non_ortho_base)
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection="3d")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    ax.scatter([0], [0], [0], color="blue", label="Origin")
    for (orig, ortho) in zip(non_ortho_base, ortho_base):
        ax.quiver(
            [0],
            [0],
            [0],
            [orig.values[0]],
            [orig.values[1]],
            [orig.values[2]],
            color="green",
        )
        ax.quiver(
            [0],
            [0],
            [0],
            [ortho.values[0]],
            [ortho.values[1]],
            [ortho.values[2]],
            color="red",
        )
    ax.view_init(10, -160)
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
