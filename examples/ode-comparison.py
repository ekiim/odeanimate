from math import sqrt, e, pi, sin, atan, cos
import matplotlib.pyplot as plt
from examples.output import output_file
from odeanimate.vector import Vector 
from odeanimate.domains import Interval
from odeanimate.plots.axes import cartesian_axes
from odeanimate.methods.ode import (
    integrate,
    runge_kutta_4,
    euler_method,
)

from odeanimate.utils import Interpolator
plt.rcParams["text.usetex"] = True


class DampedVibrationEDO:
    """
    Damped Vibration EDO Generator.
    This function returns an vector funtion matching the ODE system
    for a damped vibration phenomena. As

    x' = F(t, x)

    Where x is a Vector type,
    with first entry associated with position,
    and second entry associated with velocity.
    """
    def __init__(self, a, b, f=lambda t: 0):
        self.a, self.b = a, b
        self.force_func = f

    def approximate(self, t, h, x):
        return Vector(
            x[1],
            self.force_func(t) - (self.a**2)*x[0] - 2*self.b*x[1] 
        )

    def x(self, t):
        x_0, v_0 = self.initial_condition
        a, b = self.a, self.b
        m_1, m_2 = self.roots
        if self.discriminant > 0:
            """Overdamped"""
            return (x_0 / (m_1 - m_2))*(m_1 e**(m_2*t) - m_2 e**(m_1*t))
        elif self.discriminant < 0:
            """ODamped Oscilation"""
            alpha = (-self.discriminant)**(1/2)
            theta = atan(b / alpha)
            return (x_0*((alpha**2 + b**2)**(1/2))/alpha)*(e**(-b*t))*cos(alpha*t - theta)
        else:
            """Critically Dammped"""
            return x_0*(e**(-a*t))*(1 + a*t)
    
    @property
    def discriminant(self):
        a, b = self.a, self.b
        return b**2 - a**2

    @property
    def roots(self):
        a, b = self.a, self.b
        disc_root = self.discriminant**(1/2)
        return -b + disc_root, -b - disc_root 

    @classmethod
    def from_rlc(cls, R, L, C, E=lambda t: 0)
        a = 1/(L*C)
        b = R / L
        f = lambda t: E(t) / L
        return cls(a, b, f)

    @classmethod
    def from_spring(cls, m, c, k, f):
        a = k / mE
        b = c / (2*m)
        f = lambda t: f(t) / m
        return cls(a, b, f)


if __name__ == '__main__':
    R, L, C = 1e3, 1e-4, 1e-5 
    b, w = R/(2*L), (L*C)**(-1/2)
    if b**2 > w^2:
        print("")

    E_0, frec = 1, (L*C)**(-1/2) * 2
    E = lambda t: E_0*sin(frec*t)
    circuit = RLC_Generator(R, L, C, E)
    interval = Interval(0, 1/w_eff)
    initial_condition = Vector(
        0, # Initial Charge
        0, # Initial Current
    )
    steps = 100000
    h = interval.__len__() / steps
    integrator = integrate(
            runge_kutta_4,
            circuit,
            h,
            *interval.limits,
            initial_condition,
    )
    fig = plt.figure(figsize=(18, 6))
    axes_args = (interval, Interval(-10, 10))
    E_ax = cartesian_axes(
        fig.add_subplot(3, 1, 1),
        *axes_args
    )
    E_ax.set_title("Source")
    Q_max_cap = max((C*E_0, 1))
    Q_ax = cartesian_axes(
        fig.add_subplot(3, 1, 2),
        interval, Interval(-Q_max_cap, Q_max_cap)
    )
    Q_ax.set_title("Charge")
    I_max_ohm = max((1.2*(E_0 / R), 1))
    I_ax = cartesian_axes(
        fig.add_subplot(3, 1, 3),
        interval, Interval(-I_max_ohm, I_max_ohm)
    )
    I_ax.set_title("Current")

    T, Q, I = [], Interpolator(), Interpolator()
    x_next = initial_condition 
    for t in interval(h):
        x_next = runge_kutta_4(circuit, h, t, x_next)
        T.append(t)
        q, i = x_next
        Q.add(t, q)
        I.add(t, i)

    E_ax.plot( T, [E(t) for t in T])
    Q_ax.plot( T, [Q(t) for t in T])
    I_ax.plot( T, [I(t) for t in T])
    image_file = output_file(__file__, ".png")
    fig.savefig(image_file, dpi=300)

