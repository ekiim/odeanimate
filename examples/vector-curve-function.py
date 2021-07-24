from math import sin, cos, pi
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.vector import Vector


@Vector.codomain
def helicoid(t):
    return 3*cos(2*pi*t), 2*sin(2*pi*t), 3*t/4


if __name__ == '__main__':
    x_0, x_N = -2, 2
    N = 100
    dx = (x_N-x_0)/N
    dt = [x_0+i*dx for i in range(N+1)]
    X, Y, Z = [helicoid(j).values[0] for j in dt], \
              [helicoid(j).values[1] for j in dt], \
              [helicoid(j).values[2] for j in dt]
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-5, 5)
    ax.plot(X, Y, Z, c=(0.25, 1.00, 0.25))
    image_file = output_file(__file__, '.png')
    fig.savefig(image_file)
