from math import sin
from odeanimate.domains import Interval
from odeanimate.curve import Curve1D
import matplotlib.pyplot as plt
from examples.output import output_file


@Curve1D
def polynomial(x):
    # return(x - 5)*(x - 3)*(x+1) / 4
    return ((2+x)**0.5)*sin(x/2) - 1.5


if __name__ == '__main__':
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot()
    x_lim = [-5, 5]
    y_lim = [-5, 5]
    f = polynomial
    interval = Interval(-1, 5)
    f_eval = list(map(f, interval))
    X, Y = list(interval), f_eval
    ax.plot(X, Y)
    ax.fill_between(
        X, Y,
        where=list(map(lambda x: x in interval and f(x) > 0, X))
    )
    ax.fill_between(
        X, Y,
        where=list(map(lambda x: x in interval and f(x) < 0, X))
    )

    ax.set_xlim(*x_lim)
    ax.set_ylim(*y_lim)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    image_file = output_file(__file__, '.png')
    fig.savefig(image_file)
