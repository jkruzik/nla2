# %% [markdown]
# ## Estimating Pi using Monte Carlo method
# https://en.wikipedia.org/wiki/Monte_Carlo_method#Overview
# %%
from mpi4py import MPI
import random
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Default number of tosses
tosses = 1000000
if len(sys.argv) > 1:
    tosses = int(round(float(sys.argv[1])))

# Divide work
local_tosses = tosses // size
local_count = 0

random.seed(rank)  # unique seed per rank

for _ in range(local_tosses):
    x, y = random.random(), random.random()
    if x*x + y*y <= 1.0:
        local_count += 1

# Reduce results
global_count = comm.reduce(local_count, op=MPI.SUM, root=0)

if rank == 0:
    pi_estimate = (4.0 * global_count) / tosses
    print(f"Estimated π = {pi_estimate:.6f} using {tosses} tosses and {size} processes")

