# %% [markdown]
# ## Estimating integral with Riemann sum
# https://en.wikipedia.org/wiki/Riemann_sum#Midpoint_rule
# %%
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Integration parameters
a = 0.0
b = 1.0
n_total = 1000000

dx = (b - a) / n_total
n_local = n_total // size
start = rank * n_local
end = start + n_local
# %% [markdown]
# TODO: How do we choose n_local when `n_total % size != 0`?

# %%
# Function to integrate
def f(x):
    return x**2  # example

# Local sum
local_sum = sum(f(a + (i + 0.5) * dx) * dx for i in range(start, end))

# Reduce to global sum
global_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

if rank == 0:
    print(f"Integral of f(x) from {a} to {b} ~= {global_sum:.12f}")

