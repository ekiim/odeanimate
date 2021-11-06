from pathlib import Path

# Constant used as base deltas.
h = 0.001
tolreance = 0.000001


def dense_range(start, end, step=1):
    cur = start
    while abs(end - cur) < tolreance:
        yield cur
        cur += step


class DenseRange:

    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step
        self.current = start

    def clone(self):
        return self.__class__(self.start, self.end, self.step)

    def __iter__(self):
        return self.clone()

    def __next__(self):
        if abs(self.end - self.current) < tolreance:
            raise StopIteration
        returnable = self.current
        self.current += self.step
        return returnable


def output_file(file, ext, project_root=Path(__file__).parent.parent):
    assets_dir = project_root / 'assets'
    assets_dir.mkdir(exist_ok=True)
    return str(assets_dir / (Path(file).stem + ext))
