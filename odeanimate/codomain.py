from odeanimate.vector import Vector


class Trajectory:
    def __init__(self, *args, keys=None, **kwargs):
        if any((not Vector.is_compatible(v) for v in args)):
            raise Exception("Incompatible Object")
        rows = tuple(Vector.from_compatible(v) for v in args)
        if len(set(len(v) for v in rows)) != 1:
            raise Exception("Inconsistent row found")
        self._rows = rows
        self._shape = (len(rows), len(rows[0]))
        self.set_keys(keys)

    def set_keys(self, keys=None):
        if keys is None:
            keys = [f"col_{i}" for i in range(1, self._shape[1] + 1)]

        if any((not isinstance(k, str) for k in keys)):
            raise Exception("Keys are not strings")
        self._keys = tuple(keys)

    def get_column_by_key(self, *keys):
        if len(keys) == 1:
            key = keys[0]
        if key in self._keys:
            index = self._keys.index(key)
            return Vector(*[v[index] for v in self._rows])
        raise Exception("Multiple keys not supported yet")

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __repr__(self):
        rows, cols = self._shape
        return f"<Trajectory rows={rows} cols={cols} keys={self._keys}>"

    def __getattr__(self, name):
        return self.get_column_by_key(name)
        raise Exception("Attribute doesn't exist in keys")

    def _repr_html_(self):
        keys = self._keys
        return "".join(
            [
                "<table>",
                "<thead>",
                "<tr>",
                *[f"<th>${k}$</th>" for k in keys],
                "</tr>",
                "</thead>",
                "<tbody>",
                *[
                    "".join(["<tr>", *[f"<td>{str(x)}</td>" for x in row], "</tr>"])
                    for row in self._rows
                ],
                "</tbody>",
                "</table>",
            ]
        )

    def _ipython_display_(self):
        return self._repr_html_()

    def _plot_2d(self, ax, keys=["x", "y"], **kwargs):
        x = getattr(self, keys[0])
        y = getattr(self, keys[1])
        ax.plot(x, y)

    def _plot_3d(self, ax, keys=["x", "y", "z"], **kwargs):
        x = getattr(self, keys[0])
        y = getattr(self, keys[1])
        z = getattr(self, keys[2])
        ax.plot(x, y, z)
