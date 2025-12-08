import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

def cg_poly(A, b=None, u=None, epsilon=1e-6, maxit=100):
    n = len(A)
    if b is None: b = np.ones(n)
    if u is None: u = np.zeros(n)

    r = b - A @ u
    d = r.copy()
    rho = np.dot(r, r)
    rho_0 = rho
    rho_prev = rho

    beta = 0.0

    res_history = []
    E_pol_history = []

    P_one = Polynomial([1])
    P_x = Polynomial([0, 1])

    E_prev = None
    D_prev = None

    for i in range(1, maxit + 1):
        w = A @ d
        denom = np.dot(w, d)
        if denom == 0: break
        alpha = rho_prev / denom

        term_res = P_one - alpha * P_x
        if i == 1:
            E_curr = term_res
        else:
            E_curr = term_res * E_prev + (alpha * beta) * D_prev

        E_pol_history.append(E_curr)

        u = u + alpha * d
        r = r - alpha * w
        rho = np.dot(r, r)

        res_history.append(rho / rho_0)

        if rho <= epsilon**2 * rho_0:
            break

        if i == 1:
            # P_0 = R_0 (since d_0 = r_0). R_0 = 1.
            # D_1 corresponds to -x * P_0 = -x * 1
            D_curr = -P_x
        else:
            D_curr = -P_x * E_prev + beta * D_prev

        beta = rho / rho_prev

        rho_prev = rho
        d = r + beta * d

        E_prev = E_curr
        D_prev = D_curr

    return u, res_history, E_pol_history

# diag
n = 5
diag_values = np.arange(1, n + 1, dtype=float)
A = np.diag(diag_values)

# rand
#A = np.random.randn(n,n)
#A = A.T @ A + np.eye(n)*0.1

b = np.ones(n)
u_sol, res, polys = cg_poly(A, b, epsilon=1e-16,maxit=n+2)

plt.figure(figsize=(12, 6))
eigvals = np.linalg.eigvalsh(A)
x_vals = np.linspace(0, eigvals[-1] + .1*(eigvals[-1] - eigvals[0])/len(eigvals), 500)
for idx, p in enumerate(polys):
    y_vals = p(x_vals)
    plt.plot(x_vals, y_vals, label=f'Iter {idx+1}', alpha=0.8)
    print(f"{p(eigvals)} sum = {sum(abs(p(eigvals)))}") # note that the sum() may increase!

# Highlight Eigenvalues
plt.scatter(eigvals, np.zeros_like(eigvals), color='red', zorder=10, marker='x', s=100, label='Eigenvalues')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')

plt.xlabel('Eigenvalues')
plt.ylabel('P(x)')
plt.ylim(-2, 2) # Limit y-axis to see the roots clearly, as polynomials grow large outside roots
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("Error:", np.linalg.norm(np.linalg.solve(A, b)-u_sol))
