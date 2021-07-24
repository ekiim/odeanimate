import matplotlib.pyplot as plt
from odeanimate.vector import Vector
from examples.output import output_file


if __name__ == '__main__':
    a = Vector(1, 2, 3)
    b = Vector(3, 2, 1)
    print(a + b)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-5, 5)
    ax.quiver([0],[0],[0], [a.values[0]], [a.values[1]], [a.values[2]])
    image_file = output_file(__file__, '.png')
    fig.savefig(image_file)
