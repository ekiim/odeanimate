"""Integration Methods

All this function resemble integration methods, and they must maintain the same
interface.

---

Dev Notes:

    - might be a good idea to implement darboux sum too, but inf and sup might
    be problematic.

"""


def riemann_variant_step(variant, x, step):
    returnable = x
    if variant == "left":
        pass
    if variant == "mid":
        returnable += step / 2
    if variant == "right":
        returnable += step
    return returnable


def riemann_variant(variant, f, x, step):
    returnable = 0
    if variant == "left":
        returnable = riemann_left(f, x, x + step)
    elif variant == "mid":
        returnable = riemann_mid(f, x, x + step)
    elif variant == "right":
        returnable = riemann_right(f, x, x + step)
    else:
        raise Exception("Unknown variant")
    return returnable


def riemann_left(f, a, b):
    return (b - a) * f(a)


def riemann_right(f, a, b):
    return (b - a) * f(b)


def riemann_mid(f, a, b):
    return (b - a) * f((a + b) / 2)


def trapezoidal_rule(f, a, b):
    return (b - a)(f(b) + f(a)) / 2


def simpson_first_rule(f, a, b):
    return ((b - a) / 6) * (f(a) + 4 * f((a + b) / 2) + f(b))


def simpson_second_rule(f, a, b):
    return ((b - a) / 8) * (
        f(a) + 3 * f((2 * a + b) / 3) + 3 * f((a + 2 * b) / 3) + f(b)
    )
