from math import sin, cos, PI
import matplotlib.pyplot as plt
from odeanimate.vector import Vector

@Vector.codomain
def helicoid(t):
    return 3*cos(2*PI*t), 2*sin(2*PI*t), 3*t/4

if __name__ == '__main__':
    pass
