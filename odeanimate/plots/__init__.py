from distutils.spawn import find_executable
import matplotlib.projections as proj
import matplotlib.pyplot as plt
from odeanimate.plots.axes import ODEAnimateAxes, ODEAnimateAxes3D

if find_executable("latex"):
    plt.rcParams["text.usetex"] = True

proj.register_projection(ODEAnimateAxes)
proj.register_projection(ODEAnimateAxes3D)
