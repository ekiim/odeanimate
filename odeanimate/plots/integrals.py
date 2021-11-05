def riemann_variant(variant, x, step):
    returnable = x
    if variant == 'left':
        pass
    if variant == 'mid':
        returnable += step/2
    if variant == 'right':
        returnable += step
    return returnable

def riemann_sum(
    ax,
    f,
    interval,
    n,
    domain=None,
    variant="left",
    rectangle_color="g"
):
    if not domain:
        domain = interval
    f_eval = list(map(f, interval))
    X, Y = list(interval), f_eval
    step = len(interval) / n
    ax.plot(X, Y)
    for x in interval(step):
        eval_x = riemann_variant(variant, x, step)
        ax.plot(
            [x, x, x+step, x+step],
            [0, f(eval_x), f(eval_x), 0],
            c=rectangle_color
        )
    return ax
