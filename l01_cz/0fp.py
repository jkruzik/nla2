# %% [markdown]
# ## Zaokrouhlování
# %%
def eprint(expr, mid=" "):
    print(expr, mid, eval(expr))


a = 0.1 + 0.2
b = 0.3
eprint("a == b ")

# %% [markdown]
# ## Jak porovnat čísla s plovoucí řadovou čárkou?
# %%
eps = 1e-15  # viz také https://en.wikipedia.org/wiki/Machine_epsilon
print(abs(a - b))
print(abs(a - b) <= eps)

# %% [markdown]
# absolutní odchylka, nemusí fungovat vždy
# %%
import math

a = 1e300
b = math.nextafter(a, math.inf)  # vrací nejbližší reprezovatelné číslo
print(a, b)
print("rozdíl: ", abs(a - b))
print("blízko sebe: ", abs(a - b) <= eps)
# %% [markdown]
# relativní odchylka
# %%
print("blízko sebe (relativně): ", abs(a - b) / min(a, b) < eps)

# %% [markdown]
# Co kdyby b = 0?
# Relativní odchylka nemá smysl (i kdybychom vyřešili dělení nulou).
# Čísla, která považujeme blízkov v rámci absolutní ochylky závisí na kontextu, odkud jsme čísla získali.
# Viz [boost](https://www.boost.org/doc/libs/latest/libs/math/doc/html/math_toolkit/float_comparison.html) a [boost2](https://www.boost.org/doc/libs/latest/libs/test/doc/html/boost_test/testing_tools/extended_comparison/floating_point/floating_points_comparison_theory.html)

# %% [markdown]
# ## Asociativity
# %%
eprint("(1e16 - 1e16) + 1.0 == 1.0")
eprint("1e16 + (-1e16 + 1.0) == 1.0")
eprint("(1e300 * 1e300) * 1e-300", " = ")
eprint("1e300 * (1e300 * 1e-300)", " = ")

# %% [markdown]
# Viz také [Floating-Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html), případně [Interval arithmetic](https://en.wikipedia.org/wiki/Interval_arithmetic)
