from math import cos, exp
from sys import stderr
from odeanimate.curve import Curve1D


@Curve1D
def x_inverse(x):
    return 1 / x


@Curve1D
def natural_logarithm(x):
    return x_inverse.integrate(1, x, h=0.1)


if __name__ == "__main__":
    print("x,e^x,ln(e^x)")
    for i in range(1, 10):
        e = exp(i)
        print(i, e, natural_logarithm(e), sep=",")

    print(x_inverse._function.cache_info(), file=stderr)
