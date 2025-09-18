# %% [markdown]
# ## Příklad výpočtu obsahu jehlovitých trojúhelníků.
# reference [W. Kahan "Miscalculating Area and Angles of a Needle-like Triangle" (2014)](https://people.eecs.berkeley.edu/~wkahan/Triangle.pdf)
# %%
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from mpmath import mp, mpf, sqrt as mpsqrt


# %% [markdown]
# Heronův vzorec
# %%
def heron_area(a, b, c):
    s = 0.5 * (a + b + c)
    val = s * (s - a) * (s - b) * (s - c)
    if val <= 0:
        return 0.0
    return math.sqrt(val)


# %% [markdown]
# Stabilní vzorec, musí platit a >= b >= c
# %%
def kahan_area(a, b, c):
    # Seřaď straně sestupně: a >= b >= c
    sides = sorted([a, b, c], reverse=True)
    a, b, c = sides
    if a >= b + c:
        return 0.0
    t1 = a + (b + c)
    t2 = c - (a - b)
    t3 = c + (a - b)
    t4 = a + (b - c)
    prod = t1 * t2 * t3 * t4
    if prod <= 0:
        return 0.0
    return 0.25 * math.sqrt(prod)


# %% [markdown]
# Pomocí knihovny mpmath můžeme počítat s libovolnou přesností.
# %%
mp.dps = 80  # vysoká přesnost pro vzorový výpočet (desetiná místa)


def mp_heron_area(a, b, c):
    a, b, c = mp.mpf(a), mp.mpf(b), mp.mpf(c)
    s = (a + b + c) / 2
    val = s * (s - a) * (s - b) * (s - c)
    if val <= 0:
        return mp.mpf("0")
    return mpsqrt(val)


# %% [markdown]
# TODO měňte hodnoty a zjistěte jak moc špatný výsledek můžete získat, následně se podívejte na ukázky v referenci
# %%
a = 9.0
b = 4.53
c = b

h = heron_area(a, b, c)
k = kahan_area(a, b, c)
m = mp_heron_area(a, b, c)

print(
    f"Heronův obsah {h}, absolutní chyba: {float(h - m):.17e}, relativní chyba: {float((h - m) / m):.2e}"
)
print(
    f"Kahanův obsah {k}, absolutní chyba: {float(k - m):.17e}, relativní chyba: {float((k - m) / m):.2e}"
)
