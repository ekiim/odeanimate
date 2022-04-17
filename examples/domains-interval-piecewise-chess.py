import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes


def pawn(x):
    if x in Interval(1, 1.5):
        return 1
    elif x in Interval(1.5, 2):
        return 1 / 2
    elif x in Interval(2, 3):
        # from (a, b) to (c, d)
        # d + (b - d)/(a - c))*(x - c)
        a, b, c, d = 2, 1 / 2, 3, 1 / 3
        return d + ((b - d) / (a - c)) * (x - c)
        # return (1/2) + ((1/2 - 1/3)/(neck.lower - neck.upper))*(x - 2)
    elif x in Interval(3, 4):
        r, h, k = 1 / 2, 3, 1 / 3
        return (r**2 - (x - h - r) ** 2) ** (1 / 2) + k
    return 0


def bishop(x):
    if x in Interval(1, 1.5):
        return 1
    elif x in Interval(1.5, 2):
        a, b, c, d = 1.5, 1 / 2, 2, 0.4
        return d + ((b - d) / (a - c)) * (x - c)
    elif x in Interval(2, 4):
        a, b, h, k = 1, 0.5, 3, 0.4
        return (1 / a) * ((a * b) ** 2 - (b * (x - h)) ** 2) + k
    elif x in Interval(4, 5):
        a, b, h, k = 0.5, 0.75, 4.5, 0.4
        return (1 / a) * ((a * b) ** 2 - (b * (x - h)) ** 2) + k
    return 0


if __name__ == "__main__":
    fig = plt.figure(figsize=(16, 16))
    step = 1 / 100
    x_int, y_int = Interval(0.5, 5.5), Interval(-0.25, 1.75)
    x_points = list(x_int(step))
    pieces = [pawn, bishop]
    for i, piece in enumerate(pieces, start=1):
        axes = cartesian_axes(
            fig.add_subplot(len(pieces), 1, i, aspect=1), x_int, y_int
        )
        y_points = [piece(x) for x in x_int(step)]
        axes.plot(x_points, y_points)
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file)
