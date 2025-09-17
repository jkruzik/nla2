# %% [markdown]
# ## Conditioning
# Evaluate [Wilkinson's polynomial](https://en.wikipedia.org/wiki/Wilkinson's_polynomial) in its roots
# %%
import numpy as np
from sympy import Symbol
from sympy.polys.polytools import   poly_from_expr

x = Symbol('x')
W = 1
for i in range(1, 21):
    W = W * (x-i)

P,d = poly_from_expr(W.expand())
p = P.all_coeffs()
x = np.arange(1, 21)
print("These are the known roots\n",x)
print("Polynomial at roots (int) \n{}".format(np.polyval(p, x)))

# %% [markdown]
# What if the computation is done in double?
# %%
x = np.arange(1, 21, dtype=np.float64)
print("\nPolynomial at roots (double) \n{}".format(np.polyval(p, x)))

# %% [markdown]
# The computation gets promoted to double, but...
# %%
print("Coefficients of the polynomial:")
print('{:<30s}{:<30s}{}'.format('Integer','Float','delta'))
for pj in p:
    print('{:<30}{:<30f}{}'.format(int(pj), float(pj), pj - int(float(pj))))

# %% [markdown]
# Relatively small changes to the coefficients cause the evaluated polynomial to blow up because it is ill conditioned.
