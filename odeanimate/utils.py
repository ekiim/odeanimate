def dense_range(start, end, step=1):
    cur = start
    while cur < end:
        yield cur
        cur += step
