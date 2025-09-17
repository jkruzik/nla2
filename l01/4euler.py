# %% [markdown]
# ## Error Accumulation
# Using simple [Euler method](https://en.m.wikipedia.org/wiki/Euler_method) for solving ODE
# %%
import numpy as np
import matplotlib.pyplot as plt

def f(y, t):
    """ODE function: y' = -100y + 100t + 101"""
    return -100 * y + 100 * t + 101

def euler(y0, h, n_steps):
    """Euler method for solving y' = f(y,t)"""
    y = np.zeros(n_steps + 1)
    t = np.zeros(n_steps + 1)

    # initial condition
    y[0] = y0
    t[0] = 0.0

    for k in range(n_steps):
        y[k+1] = y[k] + h * f(y[k], t[k])
        t[k+1] = (k+1) * h

    return t, y

# %% [markdown]
# The first few iterations are supposed to be
# $$
# \begin{align*}
#    y_0 &= 1\\
#    y_1 &= 1 +   0.1(-100 \cdot 1  + 100 \cdot 0.0 + 101) = 1.1\\
#    y_2 &= 1.1 + 0.1(-100 \cdot 1.1  + 100 \cdot 0.1 + 101) = 1.2\\
#    y_3 &= 1.1 + 0.1(-100 \cdot 1.2 + 100 \cdot 0.2 + 101) = 1.3\\
# \end{align*}
# $$
# It is easy to simplify the iterates
# %%
def euler_stab(y0, h, n_steps):
    """Euler method for solving y' = f(y,t)"""
    y = np.zeros(n_steps + 1)
    t = np.zeros(n_steps + 1)

    # initial condition
    y[0] = y0
    t[0] = 0.0

    for k in range(n_steps):
        y[k+1] = 1 + h * (k+1)
        t[k+1] = (k+1) * h

    return t, y


# %%
# Parameters
y0 = 1       # initial condition
h = 0.1      # step size
n_steps = 20 # number of iterations

t, y_euler = euler(y0, h, n_steps)
_, y_euler_stab = euler_stab(y0, h, n_steps)
print(y_euler)
print(y_euler_stab)

