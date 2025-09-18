# %% [markdown]
# ## Hromadění chyb
# Stejně jako předchozí ukázka, ale v single (32-bit) přesnosti.
# %%
import numpy as np
import matplotlib.pyplot as plt


def f(y, t):
    """funkce ODR: y' = -100y + 100t + 101"""
    # zajisti výstup v 32-bitové přesnosti
    return np.float32(-100.0) * y + np.float32(100.0) * t + np.float32(101.0)


def euler(y0, h, n_steps):
    """Eulerova metoda pro řešení y' = f(y,t) s float32 přesností"""
    y = np.zeros(n_steps + 1, dtype=np.float32)
    t = np.zeros(n_steps + 1, dtype=np.float32)

    # Počáteční podmínky
    y[0] = np.float32(y0)
    t[0] = np.float32(0.0)
    h = np.float32(h)

    for k in range(n_steps):
        y[k + 1] = y[k] + h * f(y[k], t[k])
        t[k + 1] = (k + 1) * h

    return t, y


def euler_stab(y0, h, n_steps):
    """Eulerova metoda pro řešení y' = f(y,t) s float32 přesností"""
    y = np.zeros(n_steps + 1, dtype=np.float32)
    t = np.zeros(n_steps + 1, dtype=np.float32)

    # Počáteční podmínky
    y[0] = np.float32(y0)
    t[0] = np.float32(0.0)
    h = np.float32(h)

    for k in range(n_steps):
        y[k + 1] = y0 + h * np.float32(k + 1)
        t[k + 1] = (k + 1) * h

    return t, y


# Parametry
y0 = 1  # počáteční podmínka
h = 0.1  # velikost kroku
n_steps = 20  # počet iterací

t, y = euler(y0, h, n_steps)
t, y_stab = euler_stab(y0, h, n_steps)
print(y)
print(y_stab)
