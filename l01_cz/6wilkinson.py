# %% [markdown]
# ## Předpodmínění
# Vypočtěte [Wilkinsonův mnohočlen](https://en.wikipedia.org/wiki/Wilkinson's_polynomial) v jeho kořenech.
# %%
import numpy as np
from sympy import Symbol
from sympy.polys.polytools import poly_from_expr

x = Symbol("x")
W = 1
for i in range(1, 21):
    W = W * (x - i)

P, d = poly_from_expr(W.expand())
p = P.all_coeffs()
x = np.arange(1, 21)
print("Toto jsou známé kořeny\n", x)
print("Mnohočlen vypočten v kořenech (int) \n{}".format(np.polyval(p, x)))

# %% [markdown]
# Co kdybychom počítali s doubly (64-bit)?
# %%
x = np.arange(1, 21, dtype=np.float64)
print("\nMnohočlen v kořenech (double) \n{}".format(np.polyval(p, x)))

# %% [markdown]
# Výpočet se provede v doublech, ale...
# %%
print("Coefficients of the polynomial:")
print("{:<30s}{:<30s}{}".format("Integer", "Float", "delta"))
for pj in p:
    print("{:<30}{:<30f}{}".format(int(pj), float(pj), pj - int(float(pj))))

# %% [markdown]
# poměrně malé změny koefficientů zapříčiní, že výsledek nabyde velkých rozměrů, protože je mnohočlen špatně podmíněný.
