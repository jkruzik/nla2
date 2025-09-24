# %% [markdown]
# ## Matrix-vector product with dense matrix
# We simply gather the vector to be multiplied and then essentially perform the now local dot product.
# By default, this setup needs about 3.2 GB of memory (see `n_global`, `m_global`)
# %%
from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# make a tall and skinny matrix so that we can see some speedup
m_global = 2000000
n_global = 200
# TODO fix m_global % != 0
if m_global % size != 0:
    if rank == 0:
        print(f"m_global = {n_global} not divisible by size = {size}")
    sys.exit(1)
if n_global % size != 0:
    if rank == 0:
        print(f"n_global = {n_global} not divisible by size = {size}")
    sys.exit(1)

m_local = m_global // size
n_local = n_global // size

# Local rows of A: n_local x m_global
A_local = np.random.rand(m_local, n_global)

# Local part of x
x_local = np.full(n_local, fill_value=1, dtype='d')

# %%
comm.Barrier()
start = MPI.Wtime()
# Gather full x on all ranks
x_full = np.empty(n_global, dtype='d')
comm.Allgather(x_local, x_full)

# Local matvec
y_local = A_local @ x_full
comm.Barrier()
end = MPI.Wtime()

if (rank == 0): print(f"The {m_global}x{n_global} matmult on {size} ranks took:{end - start} s")

# %%
# TODO If we imagine a block-diagonal partitioning of the matrix, e.g.,
#            1  2  0  |  0  3  0  |  0  4
#    Proc0   0  5  6  |  7  0  0  |  8  0
#            9  0 10  | 11  0  0  | 12  0
#    -------------------------------------
#           13  0 14  | 15 16 17  |  0  0
#    Proc1   0 18  0  | 19 20 21  |  0  0
#            0  0  0  | 22 23  0  | 24  0
#    -------------------------------------
#    Proc2  25 26 27  |  0  0 28  | 29  0
#           30  0  0  | 31 32 33  |  0 34
# we can write such a block matrix as [A B C
#                                      D E F;
#                                      H I G]
# Then we can multiply the block diagonal parts of the matrix (A, E, and G) with our local vector without any communication.
# Therefore, we can overlap the communication of the vector x with the local part of the matrix multiplication.
# Use the immediate return `MPI.Iallgatherv()` to obtain the vector x from other ranks.
# Compute the local matrix-vector product, e.g., E*x_local.
# `MPI.Wait()` for the Iallgatherv to complete.
# Compute the matrix-vector products with the non-block diagonal parts of the matrix and correctly sum up the results to y_local.
