# %% [markdown]
# ## Gaussian elimination needs pivoting
# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import hilbert, solve

def gaussian_elimination(A, b):
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)

    for k in range(n-1):
        if A[k, k] == 0:
            raise ValueError("Zero pivot encountered!")
        for i in range(k+1, n):
            factor = A[i, k] / A[k, k]
            A[i, k:] = A[i, k:] - factor * A[k, k:]
            b[i] = b[i] - factor * b[k]

    # Back substitution
    x = np.zeros(n)
    for i in reversed(range(n)):
        x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i, i]

    return x


def relative_error(x_true, x_computed):
    return np.linalg.norm(x_true - x_computed) / np.linalg.norm(x_true)

def backward_error(A, b, x):
    return np.linalg.norm(b - A @ x)/(np.linalg.norm(b) + np.linalg.norm(A,2)*np.linalg.norm(x))


# %%
eps = 1e-16
H = np.array([[eps, 1.], [1., 1.]])
x_exact = np.array([2 - (1-2*eps)/(1-eps), (1-2*eps)/(1-eps)]) # for b = [1 2]
b = H @ x_exact

x_naive  = gaussian_elimination(H.copy(), b.copy())
x = solve(H, b) # direct solver with pivoting

print(f"Condition number: {np.linalg.cond(H):.2e}")
print(f"||r_exact|| =  {np.linalg.norm(H @ x_exact -b):.2e}")
print(f"||r|| =  {np.linalg.norm(H @ x -b):.2e}")
print(f"||r_naive|| =  {np.linalg.norm(H @ x_naive -b):.2e}")
print(f"Relative forward error: {relative_error(x_exact,x):.2e}")
print(f"Relative forward error (naive): {relative_error(x_exact, x_naive):.2e}")
print(f"Relative backward error: {backward_error(H, b, x):.2e}")
print(f"Relative backward error (naive): {backward_error(H, b, x_naive):.2e}")

# %% [markdown]
# Gaussian elimination is backward stable with pivoting (np.linalg.solve()), but not without it.
