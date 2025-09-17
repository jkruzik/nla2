# %% [markdown]
# ## Rounding
# %%
def eprint(expr, mid=" "):
    print(expr, mid, eval(expr))

a = 0.1 + 0.2
b = 0.3
eprint("a == b ")

# %% [markdown]
# ## How to compare FP numbers?
# %%
eps = 1e-15 # see also https://en.wikipedia.org/wiki/Machine_epsilon
print(abs(a-b))
print(abs(a-b) <= eps)

# %% [markdown]
# the absolute tolerance may not work
# %%
import math
a = 1e300
b = math.nextafter(a, math.inf) # the closest next representable number
print(a,b)
print("difference: ", abs(a-b))
print("'close': ", abs(a-b) <= eps)

# %% [markdown]
# relative tolerance
# %%
print("relatively close: ", abs(a-b)/min(a,b) < eps)

# %% [markdown]
# What if b = 0?
# The relative error is pointless (even when fixing division by zero).
# Which numbers we consider close in an absolute sense depends on the context in which they are obtained.
# See [boost](https://www.boost.org/doc/libs/latest/libs/math/doc/html/math_toolkit/float_comparison.html) and [boost2](https://www.boost.org/doc/libs/latest/libs/test/doc/html/boost_test/testing_tools/extended_comparison/floating_point/floating_points_comparison_theory.html)

# %% [markdown]
# ## Associativity
# %%
eprint("(1e16 - 1e16) + 1.0 == 1.0")
eprint("1e16 + (-1e16 + 1.0) == 1.0")
eprint("(1e300 * 1e300) * 1e-300", " = ")
eprint("1e300 * (1e300 * 1e-300)", " = ")

# %% [markdown]
# See also [Floating-Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html), optionally [Interval arithmetic](https://en.wikipedia.org/wiki/Interval_arithmetic)
