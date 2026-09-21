# %% [markdown]
# ##  MPI ping-pong
# run with `mpirun -n 2 python 3pingpong.py`
# %%
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size != 2:
    if rank == 0:
        print("This program requires exactly 2 processes")
    exit()

niter = 10000
message = 0
partner_rank = 1 - rank

print(f"Hello world from rank {rank} of {size}. My partner is {partner_rank}.")

# %% [markdown]
# The processes execute the code independently.
# As a consequence, the second process can print the above string before the first process.
# We synchronize all processes before timing
# %%
comm.Barrier()
start = MPI.Wtime()

for _ in range(niter):
    if rank == 0:
        comm.send(message, dest=partner_rank) # lowercase methods are used for python objects
        message = comm.recv(source=partner_rank)
    else:
        message = comm.recv(source=partner_rank)
        comm.send(message, dest=partner_rank)

end = MPI.Wtime()

if rank == 0:
    total_time = end - start # in seconds
    avg_time = (total_time / (2.0 * niter)) * 1e6  # one-way latency in microseconds
    print(f"Ping-pong latency: {avg_time:.3f} microseconds (avg over {niter} iterations)")

