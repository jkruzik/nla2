# %% [markdown]
# ## Solving Ill Conditioned System of Linear Equations
# %%
import numpy as np

# Define a nearly singular matrix
A = np.array([[1, 1],
              [1, 1.0001]], dtype=float)

# Define right-hand side
b = np.array([2, 2.0001], dtype=float)

# Exact solution using numpy solver
x_exact = np.linalg.solve(A, b)

# %% [markdown]
# Solution using [Cramer's rule](https://en.wikipedia.org/wiki/Cramer%27s_rule)
# %%
def cramer_rule(A, b):
    det = A[0,0]*A[1,1] - A[0,1]*A[1,0]
    x = np.array([(b[0]*A[1,1] - b[1]*A[0,1]) / det,
                  (A[0,0]*b[1] - A[1,0]*b[0]) / det])
    return x

x_cramer = cramer_rule(A, b)

# %% [markdown]
# Perturb b slightly
# %%
b_perturbed = b + np.array([1e-5, -1e-5])
x_perturbed = np.linalg.solve(A, b_perturbed)

# %% [markdown]
# Print results
# %%
print("Matrix A:")
print(A)
print("\nOriginal b:", b)
print("Solution (numpy):", x_exact)
print("Solution (Cramer):", x_cramer)
print("\nPerturbed b:", b_perturbed)
print("Solution for perturbed b:", x_perturbed)

def forward_error(x_true, x_computed):
    return np.linalg.norm(x_true - x_computed) / np.linalg.norm(x_true)

def backward_error(A, b, x):
    return np.linalg.norm(b - A @ x)/(np.linalg.norm(b) + np.linalg.norm(A,2)*np.linalg.norm(x))

print("\nRelative error in solution due to small perturbation in b:", forward_error(x_exact, x_perturbed))

# %%
# TODO compute the relative backward error.
# Is np.linalg.solve() backward stable?
print("Relative backward error:", backward_error(A, b_perturbed, x_perturbed))

# %%
# Compute the solution of perturbed system using Cramer's rule. Check the relative error and backward stability.
# Is Cramer's rule backward stable?
x_perturbed = cramer_rule(A, b_perturbed)
x_exact = np.array([1.20001, 0.8]) # by hand
print("\nRelative error in solution (Cramer):", forward_error(x_exact, x_perturbed))
print("Relative backward error (Cramer):", backward_error(A, b_perturbed, x_perturbed))

# %% [markdown]
# That is about 3 orders of magnitude above the machine precision. Is it stable? No, see below.
# %%
A = np.array([[1, 1],
              [1, 1 + 1e-15]], dtype=float)
x_exact = np.array([1, 1 + 1-15], dtype=float)
b = A @ x_exact
x = cramer_rule(A, b)
print("\nRelative error in solution (Cramer):", forward_error(x_exact, x))
print("Relative backward error(Cramer):", backward_error(A, b, x))
