# %% [markdown]
# ## Katastrofické vyrušení
# %%
import numpy as np


def naive(x, y):
    return x**2 - y**2


def stable(x, y):
    return (x - y) * (x + y)


pairs = [
    (1.0, 0.9999999),
    (1.0 + 2 ** (-29), 1.0 + 2 ** (-30)),
    (1e8, 1e8 - 1),
]

print(f"{'x':<23} {'y':<23} {'naivní':<23} {'stabilní':<23} ~správné (dec) číslice")
for x, y in pairs:
    n = naive(x, y)
    s = stable(x, y)
    rel_error = abs((n - s) / s) if s != 0 else np.nan
    digits = max(0, -np.log10(rel_error)) if rel_error > 0 else -1
    print(f"{x:.17e} {y:.17e} {n:.17e} {s:.17e} {digits}")
