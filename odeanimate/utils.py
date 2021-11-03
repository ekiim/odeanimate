h = 0.001


def dense_range(start, end, step=1):
    cur = start
    while cur < end:
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
        if self.current >= self.end:
            raise StopIteration
        returnable = self.current
        self.current += self.step
        return returnable
