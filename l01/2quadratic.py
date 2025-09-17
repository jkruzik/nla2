# %% [markdown]
# ## Catastrophic cancellation in quadratic formula
# %%
import math

def quadratic_standard(a, b, c):
    """Solve quadratic using the standard quadratic formula."""
    disc = b*b - 4*a*c
    sqrt_disc = math.sqrt(disc)
    x1 = (-b + sqrt_disc) / (2*a)
    x2 = (-b - sqrt_disc) / (2*a)
    return x1, x2

# %% [markdown]
# if $b^2 \gg ac$, then $\sqrt{b^2 - 4ac} \approx b$ and there is catastrophic
# cancellation when computing one of the roots.
# This can be fixed by expanding the fraction by the conjugate of numerator to get the sum of square ($(x+y)(x-y) = x^2 - y^2$).
# %%
def quadratic_stable(a, b, c):
    """Solve quadratic using a numerically stable approach."""
    disc = b*b - 4*a*c
    sqrt_disc = math.sqrt(disc)

    # Choose denominator to avoid cancellation
    if b > 0:
        x1 = (2*c) / (-b -sqrt_disc)
        x2 = (-b - sqrt_disc) / (2*a)
    else:
        x1 = (-b + sqrt_disc) / (2*a)
        x2 = (2*c) / (-b +sqrt_disc)

    return x1, x2


# %% [markdown]
# Example where cancellation occurs: $b^2 \gg a*c$
# %%
a, b, c = 0.0001, 100000, 0.002

roots_standard = quadratic_standard(a, b, c)
roots_stable = quadratic_stable(a, b, c)

print("Standard quadratic formula:")
print("x1 =", roots_standard[0])
print("x2 =", roots_standard[1])

print("\nNumerically stable quadratic formula:")
print("x1 =", roots_stable[0])
print("x2 =", roots_stable[1])

# %% [markdown]
# Check accuracy by plugging roots back into equation.
# Use [Horner's rule](https://en.wikipedia.org/wiki/Polynomial_evaluation) to evaluate the polynomial.
# %%
print("\nResiduals (should be ~0):")
for i, r in enumerate(roots_standard, 1):
    z = r*(a*r + b) + c
    print(f"Standard root {i}: {z:.2e}")
for i, r in enumerate(roots_stable, 1):
    z = r*(a*r + b) + c
    print(f"Stable root {i}: {z:.2e}")

print("\nRelative residuals (should be ~0):")
for i, r in enumerate(roots_standard, 1):
    z = r*(a*r + b) + c
    print(f"Standard root {i}: {abs(z)/(abs(a)*r*r + abs(b)*abs(r) + abs(c)):.2e}")
for i, r in enumerate(roots_stable, 1):
    z = r*(a*r + b) + c
    print(f"Stable root {i}: {abs(z)/(abs(a)*r*r + abs(b)*abs(r) + abs(c)):.2e}")

# %% [markdown]
# Note that if $b^2 \approx 4ac$, there is a cancellation that can only be avoided by effectively computing in extended precision.
