"""
# Roots of Unity

 - [Back](../)
"""

from math import e
from random import randint
import handout
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.utils import nth_roots_of_unity
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes

doc = handout.Handout("docs/handouts")


fig = plt.figure(figsize=(12, 12))
interval = Interval(-1.2, 1.2)
rows, cols = 4, 4
axes = [
    cartesian_axes(fig.add_subplot(rows, cols, i + 1), interval)
    for i in range(rows * cols)
]
for n, ax in enumerate(axes, start=1):
    roots = nth_roots_of_unity(n)
    x = [z.real for z in roots]
    y = [z.imag for z in roots]
    ax.scatter(x, y)

image_file = output_file(__file__, ".png")
fig.savefig(image_file)
doc.add_figure(fig)
doc.show()
