from odeanimate.matrix import Matrix


class Trajectory(Matrix):
    def __init__(self, *args, **kwargs):
        self.set_keys(kwargs.get("keys", None))
        super().__init__(*args, **kwargs)

    def set_keys(self, keys):
        if keys is None:
            keys = [f"col_{i}" for i in self._shape[1]]
        self._keys = tuple(keys)

    def __getitem__(self, key):
        # if isinstance(key, tuple):
        #    key = tuple(self._keys.index(k) for k in key)
        return super().__getitem__(key)

    def __getattr__(self, key):
        try:
            return self[key]
        except:
            return None

    def __repr__(self):
        if self._keys and len(self._keys):
            keys = f" keys={self._keys}"
        else:
            keys = ""
        try:
            rows = len(self.shape[0])
        except:
            rows = self.shape[0]
        return f"<Trayectory rows={rows}{keys}>"

    def __getattr__(self, name):
        if name not in self._keys:
            raise AttributeError
        return self[:, self._keys.index(name)]

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
                    for row in self.rows
                ],
                "</tbody>",
                "</table>",
            ]
        )
