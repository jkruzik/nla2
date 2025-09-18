# %% [markdown]
# ## Katastrofické vyrušení v kvadratické rovnici
# %%
import math


def quadratic_standard(a, b, c):
    """Vyřeš kvadratickou rovnici pomocí běžné kvadratické rovnice."""
    disc = b * b - 4 * a * c
    sqrt_disc = math.sqrt(disc)
    x1 = (-b + sqrt_disc) / (2 * a)
    x2 = (-b - sqrt_disc) / (2 * a)
    return x1, x2


# %% [markdown]
# Pokud $b^2 \gg ac$, tak $\sqrt{b^2 - 4ac} \approx b$, což vede ke Katastrofickému
# vyrušení při výpočtu jednoho z kořenů.
# Tomu se můžeme vyhnout rozšířením zlomku sdruženou verzí čitatele, abychom získali součet čtverců
# ($(x+y)(x-y) = x^2 - y^2$).
# %%
def quadratic_stable(a, b, c):
    """Vyřeš kvadratickou rovnici pomocí numericky stabilní metody."""
    disc = b * b - 4 * a * c
    sqrt_disc = math.sqrt(disc)

    # Vyber jmenovatel, abychom se vyhnuli vyrušení
    if b > 0:
        x1 = (2 * c) / (-b - sqrt_disc)
        x2 = (-b - sqrt_disc) / (2 * a)
    else:
        x1 = (-b + sqrt_disc) / (2 * a)
        x2 = (2 * c) / (-b + sqrt_disc)

    return x1, x2


# %% [markdown]
# Příklad kdy nastane katastrofické vyrušení: $b^2 \gg a*c$
# %%
a, b, c = 0.0001, 100000, 0.002

roots_standard = quadratic_standard(a, b, c)
roots_stable = quadratic_stable(a, b, c)

print("Klasická kvadratická rovnice:")
print("x1 =", roots_standard[0])
print("x2 =", roots_standard[1])

print("\nNumericky stabilní kvadratická rovnice:")
print("x1 =", roots_stable[0])
print("x2 =", roots_stable[1])

# %% [markdown]
# Kontrola přesnosti dosazením kořenů zpět do rovnice.
# Použijeme [Hornerovo schéma](https://en.wikipedia.org/wiki/Polynomial_evaluation) pro výpočet mnohočlenu.
# %%
print("\nZbytky (měli by být blízké 0):")
for i, r in enumerate(roots_standard, 1):
    z = r * (a * r + b) + c
    print(f"Běžný kořen {i}: {z:.2e}")
for i, r in enumerate(roots_stable, 1):
    z = r * (a * r + b) + c
    print(f"Stabilní kořen {i}: {z:.2e}")

print("\nRelativní zbytky (měli by být blízké 0):")
for i, r in enumerate(roots_standard, 1):
    z = r * (a * r + b) + c
    print(
        f"Běžný kořen {i}: {abs(z) / (abs(a) * r * r + abs(b) * abs(r) + abs(c)):.2e}"
    )
for i, r in enumerate(roots_stable, 1):
    z = r * (a * r + b) + c
    print(
        f"Stabilní kořen {i}: {abs(z) / (abs(a) * r * r + abs(b) * abs(r) + abs(c)):.2e}"
    )

# %% [markdown]
# Všimněte si, že pokud $b^2 \approx 4ac$, nastane vyrušení, kterému se můžeme vyhnout pouze výpočtem s větší přesností.
