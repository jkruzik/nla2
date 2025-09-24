# %% [markdown]
# ## Dot product
# This is the standard way to compute a dot product in parallel
# %%
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

n = 1000

n_local = n // size

x_local = 2*np.ones(n_local, dtype='d')
y_local = 4*np.ones(n_local, dtype='d')

local_dot = np.dot(x_local, y_local)
global_dot = comm.allreduce(local_dot, op=MPI.SUM)

print(f"Rank {rank}: local_dot = {local_dot}, global_dot = {global_dot}")

