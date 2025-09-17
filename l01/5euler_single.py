# %% [markdown]
# ## Error Accumulation
# Same as the previous example, but in single precision
# %%
import numpy as np
import matplotlib.pyplot as plt

def f(y, t):
    """ODE function: y' = -100y + 100t + 101"""
    # ensure float32 output
    return np.float32(-100.0) * y + np.float32(100.0) * t + np.float32(101.0)

def euler(y0, h, n_steps):
    """Euler method for solving y' = f(y,t) with float32 precision"""
    y = np.zeros(n_steps + 1, dtype=np.float32)
    t = np.zeros(n_steps + 1, dtype=np.float32)

    # initial condition
    y[0] = np.float32(y0)
    t[0] = np.float32(0.0)
    h = np.float32(h)

    for k in range(n_steps):
        y[k+1] = y[k] + h * f(y[k], t[k])
        t[k+1] = (k+1) * h

    return t, y

def euler_stab(y0, h, n_steps):
    """Euler method for solving y' = f(y,t) with float32 precision"""
    y = np.zeros(n_steps + 1, dtype=np.float32)
    t = np.zeros(n_steps + 1, dtype=np.float32)

    # initial condition
    y[0] = np.float32(y0)
    t[0] = np.float32(0.0)
    h = np.float32(h)

    for k in range(n_steps):
        y[k+1] = y0 + h * np.float32(k+1)
        t[k+1] = (k+1) * h

    return t, y

# Parameters
y0 = np.float32(1.0)  # initial condition
h = np.float32(0.1)  # step size
n_steps = 51         # number of iterations

t, y = euler(y0, h, n_steps)
t, y_stab = euler_stab(y0, h, n_steps)
print(y)
print(y_stab)

