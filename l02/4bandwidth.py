# %% [markdown]
# ##  MPI ping-pong measuring message latency and bandwidth
# %%
from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size != 2:
    if rank == 0:
        print("This program requires exactly 2 processes")
    exit()

partner_rank = 1 - rank
message_sizes = [1, 10, 100, 1000, 10000, int(1e5), int(1e6), int(1e7), int(1e8) ]  # bytes
niter = 1000

latencies = []
bandwidths = []

for size_bytes in message_sizes:
    # Create message
    msg = np.zeros(size_bytes, dtype='b')  # bytes array
    comm.Barrier()  # synchronize before timing
    start = MPI.Wtime()

    for _ in range(niter):
        if rank == 0:
            comm.Send([msg, MPI.BYTE], dest=partner_rank) # uppercase methods are used for buffer-like objects
            comm.Recv([msg, MPI.BYTE], source=partner_rank)
        else:
            comm.Recv([msg, MPI.BYTE], source=partner_rank)
            comm.Send([msg, MPI.BYTE], dest=partner_rank)

    end = MPI.Wtime()
    total_time = end - start
    avg_rtt = total_time / niter
    one_way_latency = avg_rtt / 2
    latencies.append(one_way_latency * 1e6)  # µs

    # Bandwidth = message size / one-way time
    bw = (size_bytes / one_way_latency) / 1e6  # MB/s
    bandwidths.append(bw)

    if rank == 0:
        print(f"Size: {size_bytes} B, latency: {one_way_latency*1e6:.2f} µs, bandwidth: {bw:.2f} MB/s")

# %%
if rank == 0:
    plt.figure(figsize=(10,4))

    plt.subplot(1,2,1)
    plt.loglog(message_sizes, latencies, 'o-')
    plt.xlabel("Message size [bytes]")
    plt.ylabel("One-way latency [µs]")
    plt.title("Ping-Pong Latency")

    plt.subplot(1,2,2)
    plt.loglog(message_sizes, bandwidths, 'o-')
    plt.xlabel("Message size [bytes]")
    plt.ylabel("Bandwidth [MB/s]")
    plt.title("Ping-Pong Bandwidth")

    plt.tight_layout()
    plt.show()

