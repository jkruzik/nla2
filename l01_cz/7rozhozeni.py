# %% [markdown]
# ## Řešení špatně podmíněných systémů lineárních rovnic
# %%
import numpy as np

# Definujme téměř singulární matici
A = np.array([[1, 1], [1, 1.0001]], dtype=float)

# Definujme pravou stranu
b = np.array([2, 2.0001], dtype=float)

# Výpočet přesného řešení pomocí numpy řešiče
x_exact = np.linalg.solve(A, b)


# %% [markdown]
# Řešení pomocí [Kramerova pravidlo](https://en.wikipedia.org/wiki/Cramer%27s_rule)
# %%
def cramer_rule(A, b):
    det = A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]
    x = np.array(
        [
            (b[0] * A[1, 1] - b[1] * A[0, 1]) / det,
            (A[0, 0] * b[1] - A[1, 0] * b[0]) / det,
        ]
    )
    return x


x_cramer = cramer_rule(A, b)

# %% [markdown]
# Rozhodíme trošku b
# %%
b_perturbed = b + np.array([1e-5, -1e-5])
x_perturbed = np.linalg.solve(A, b_perturbed)

# %% [markdown]
# Vypíšeme výsledky
# %%
print("Matice A:")
print(A)
print("\nPůvodní b:", b)
print("Řešení (numpy):", x_exact)
print("Řešení (Cramer):", x_cramer)
print("\nRozhozené b:", b_perturbed)
print("Řešení pro rozhozené b:", x_perturbed)

rel_error = np.linalg.norm(x_perturbed - x_exact) / np.linalg.norm(x_exact)
print("\nRelativní chyba v řešení, kvůli malému rozhození b:", rel_error)

# %%
# TODO vypočtěte relativní zpětnou odchylku
# Je np.linalg.solve() zpětně stabilní?
# Vypočtěte řešení rozhozeného systému pomocí Kramerova pravidla.
# Zaznamejte relativní odchylku a zpětnou stabilitu.
# Je Kramerovo pravidlo zpětně stabilní?
