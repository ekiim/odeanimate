import matplotlib.pyplot as plt

def cartesian_axes(ax, x_max, y_max, x_min=0, y_min=0, symetric=False):
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    return ax
