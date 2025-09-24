# %% [markdown]
# ## Solving ill-conditioned systems
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
sizes = [3, 5, 8, 12]
for n in sizes:
    # Test on Hilbert matrix
    H = hilbert(n)
    x_exact = np.ones(n)
    b = H @ x_exact

    x_naive  = gaussian_elimination(H.copy(), b.copy())
    x = solve(H, b) # direct solver with pivoting

    print(f"{n}x{n} Hilbert matrix with condition number: {np.linalg.cond(H):.2e}")
    print(f"||r_exact|| =  {np.linalg.norm(H @ x_exact -b):.2e}")
    print(f"||r|| =  {np.linalg.norm(H @ x -b):.2e}")
    print(f"||r_naive|| =  {np.linalg.norm(H @ x_naive -b):.2e}")
    print(f"Relative forward error: {relative_error(x_exact,x):.2e}")
    print(f"Relative forward error (naive): {relative_error(x_exact, x_naive):.2e}")
    print(f"Relative backward error: {backward_error(H, b, x):.2e}")
    print(f"Relative backward error (naive): {backward_error(H, b, x_naive):.2e}")
    print("-----")

# %% [markdown]
# [Hilbert matrices](https://en.wikipedia.org/wiki/Hilbert_matrix) are ill-conditioned.
# Observe the decoupling of the residual and the relative forward error.
# Both np.linalg.solve(), i.e., LU with pivoting, and Gaussian elimination without pivoting seem to be backward stable. However, that is not the case; see the next example.
