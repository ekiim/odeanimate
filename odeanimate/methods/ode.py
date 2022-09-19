def euler_method(func, h, t, x):
    return x + h * func(t, x)


def runge_kutta_4(f, h, t, x):
    k_1 = f(t, x)
    k_2 = f(t + h / 2, x + h * k_1 / 2)
    k_3 = f(t + h / 2, x + h * k_2 / 2)
    k_4 = f(t + h, x + h * k_3)
    return x + (h / 6) * (k_1 + 2 * k_2 + 2 * k_3 + k_4)


def integrate(method, func, h, t_start, t_end, x_start):
    current_t = t_start
    current_x = x_start
    while current_t <= t_end:
        yield current_x
        current_x = method(func, h, current_t, current_x)
        current_t += h
