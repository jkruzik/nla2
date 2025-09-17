# %% [markdown]
# ## Example of computing area of a needle-like triangles
# ref [W. Kahan "Miscalculating Area and Angles of a Needle-like Triangle" (2014)](https://people.eecs.berkeley.edu/~wkahan/Triangle.pdf)
# %%
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from mpmath import mp, mpf, sqrt as mpsqrt

# %% [markdown]
# standard formula
# %%
def heron_area(a, b, c):
    s = 0.5 * (a + b + c)
    val = s * (s - a) * (s - b) * (s - c)
    if val <= 0:
        return 0.0
    return math.sqrt(val)

# %% [markdown]
# stable formula, which needs a >= b >= c
# %%
def kahan_area(a, b, c):
    # Sort sides descending: a >= b >= c
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
# We can use arbitrary precision using mpmath library
# %%
mp.dps = 80  # high precision for reference computation (decimal places)

def mp_heron_area(a, b, c):
    a, b, c = mp.mpf(a), mp.mpf(b), mp.mpf(c)
    s = (a + b + c) / 2
    val = s * (s - a) * (s - b) * (s - c)
    if val <= 0:
        return mp.mpf('0')
    return mpsqrt(val)


# %% [markdown]
# TODO change the values and see how wrong the results can get, then see the examples in the reference
# %%
a = 9.0
b = 4.53
c = b

h = heron_area(a,b,c)
k = kahan_area(a,b,c)
m = mp_heron_area(a,b,c)

print(f"Heron area {h}, absolute error: {float(h-m):.17e}, relative error: {float((h-m)/m):.2e}")
print(f"Kahan area {k}, absolute error: {float(k-m):.17e}, relative error: {float((k-m)/m):.2e}")
