import matplotlib.projections as proj
from odeanimate.plots.axes import ODEAnimateAxes, ODEAnimateAxes3D

proj.register_projection(ODEAnimateAxes)
proj.register_projection(ODEAnimateAxes3D)
