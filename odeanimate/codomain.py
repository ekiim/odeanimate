from odeanimate.array import Array, _ArrayHTMLDisplay
from odeanimate.vector import Vector


class Trajectory(Array, _ArrayHTMLDisplay):
    _html_styles_cell = ""
    _html_axis = True

    def _get_column_name(self, index):
        returnable = f"col_{index}"
        if self._keys:
            returnable = self._keys[index]
        return returnable

    def __init__(self, *args, keys=None, **kwargs):
        if hasattr(args[0][-1], "__iter__"):
            args_super = [(*arg[:-1], *arg[-1]) for arg in args]
        else:
            args_super = args
        super().__init__(*args_super, **kwargs)
        if False and len(self._shape) != 2:
            raise Exception("Incompatible structure for trajectory.")
        if (
            keys is not None
            and hasattr(keys, "__len__")
            and len(keys) == self._shape[1]
        ):
            self._keys = tuple(keys)
        else:
            self._keys = None

    def __getitem__(self, keys):
        if keys in (self._keys or []):
            column = self._keys.index(keys)
            return super().__getitem__((slice(None, None, None), column))
        super().__getitem__(keys)

    def __getattr__(self, name):
        if name in (self._keys or []):
            column = self._keys.index(name)
            return super().__getitem__((slice(None, None, None), column))
        raise AttributeError

    def _plot_2d(self, ax, keys=["x", "y"], **kwargs):
        x = getattr(self, keys[0])
        y = getattr(self, keys[1])
        ax.plot(x, y)

    def _plot_3d(self, ax, keys=["x", "y", "z"], **kwargs):
        x = getattr(self, keys[0])
        y = getattr(self, keys[1])
        z = getattr(self, keys[2])
        ax.plot(x, y, z)

    def _repr_data(self):
        rows, cols = self._shape
        return f"rows={rows} cols={cols} keys={self._keys}"
