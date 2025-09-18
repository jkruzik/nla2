# %% [markdown]
# ## Hromadění chyby
# Použijeme jednoduchou [Eulerovu metodu](https://en.m.wikipedia.org/wiki/Euler_method) pro vyřešení ODR
# %%
import numpy as np
import matplotlib.pyplot as plt


def f(y, t):
    """funkce ODR: y' = -100y + 100t + 101"""
    return -100 * y + 100 * t + 101


def euler(y0, h, n_steps):
    """Eulerova metoda pro řešení y' = f(y,t)"""
    y = np.zeros(n_steps + 1)
    t = np.zeros(n_steps + 1)

    # počáteční podmínky
    y[0] = y0
    t[0] = 0.0

    for k in range(n_steps):
        y[k + 1] = y[k] + h * f(y[k], t[k])
        t[k + 1] = (k + 1) * h

    return t, y


# %% [markdown]
# Jak by mělo vypadat prvních pár iterací:
# $$
# \begin{align*}
#    y_0 &= 1\\
#    y_1 &= 1 +   0.1(-100 \cdot 1  + 100 \cdot 0.0 + 101) = 1.1\\
#    y_2 &= 1.1 + 0.1(-100 \cdot 1.1  + 100 \cdot 0.1 + 101) = 1.2\\
#    y_3 &= 1.1 + 0.1(-100 \cdot 1.2 + 100 \cdot 0.2 + 101) = 1.3\\
# \end{align*}
# $$
# Je zřejmé, jak je možné zjednodušit další iteraci.
# %%
def euler_stab(y0, h, n_steps):
    """Eulerova metoda pro řešení y' = f(y,t)"""
    y = np.zeros(n_steps + 1)
    t = np.zeros(n_steps + 1)

    # Počáteční podmínky
    y[0] = y0
    t[0] = 0.0

    for k in range(n_steps):
        y[k + 1] = 1 + h * (k + 1)
        t[k + 1] = (k + 1) * h

    return t, y


# %%
# Parametry
y0 = 1  # počáteční podmínka
h = 0.1  # velikost kroku
n_steps = 20  # počet iterací

t, y_euler = euler(y0, h, n_steps)
_, y_euler_stab = euler_stab(y0, h, n_steps)
print(y_euler)
print(y_euler_stab)
