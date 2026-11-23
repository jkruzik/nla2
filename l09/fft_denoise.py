import time
import numpy as np
import matplotlib.pyplot as plt


def build_dft_matrix(N):
    """Build the dense N x N DFT matrix (F_N)_{j,k} = exp(-2*pi*i * j*k / N)."""
    j = np.arange(N).reshape(-1, 1)
    k = np.arange(N).reshape(1, -1)
    omega = np.exp(-2j * np.pi / N)
    return omega ** (j * k)


# ============================================================================
# 1. Construct a 1D signal (sum of 3 sinusoids) corrupted by Gaussian noise
# ============================================================================
np.random.seed(42)
N = 1024  # N = 2^10 samples
t = np.arange(N) / N  # time grid on [0, 1)

# Clean signal: 3 frequencies (f1 = 5 Hz, f2 = 20 Hz, f3 = 60 Hz)
f1, f2, f3 = 5, 20, 60
x_clean = (
    1.5 * np.cos(2 * np.pi * f1 * t)
    + 1.0 * np.sin(2 * np.pi * f2 * t)
    + 0.7 * np.cos(2 * np.pi * f3 * t)
)

# TODO vary noise_std and threshold
noise_std = 1.8
noise = np.random.normal(0.0, noise_std, size=N)
x_noisy = x_clean + noise

# ============================================================================
# 2. Verify Unitary DFT Matrix properties and Parseval's Identity
# ============================================================================
F_N = build_dft_matrix(N)
unitary_err = np.linalg.norm((F_N.conj().T @ F_N) / N - np.eye(N), ord=2)

# Unitary Fourier transform: c = (1 / sqrt(N)) * F_N * x  (norm="ortho" in np.fft)
c_dft = (F_N @ x_noisy) / np.sqrt(N)
c_fft = np.fft.fft(x_noisy, norm="ortho")
fft_diff = np.linalg.norm(c_dft - c_fft)

print(f"Signal length N = {N} (2^{int(np.log2(N))})")
print(f"Unitarity check ||(1/N) F_N^H F_N - I||_2 = {unitary_err:.2e}")
print(f"Difference ||(F_N @ x)/sqrt(N) - np.fft.fft(x, norm='ortho')||_2 = {fft_diff:.2e}")
print(f"Parseval's identity: ||x_noisy||_2^2 = {np.linalg.norm(x_noisy)**2:.4f}, "
      f"||c_fft||_2^2 = {np.linalg.norm(c_fft)**2:.4f}\n")

# ============================================================================
# 3. Denoising via Orthogonal Projection (Hard Thresholding in Fourier Basis)
# ============================================================================
# In unitary normalization, white noise of std sigma has expected magnitude ~ sigma per mode
# TODO use MAD to estimate noise_std
threshold = 3.5 * noise_std
keep_mask = np.abs(c_fft) >= threshold
c_thresh = np.where(keep_mask, c_fft, 0.0)

# Reconstruct via inverse unitary transform: x_tilde = (1 / sqrt(N)) * F_N^H * c_thresh
x_denoised = np.real(np.fft.ifft(c_thresh, norm="ortho"))

# Verify exact 2-norm thresholding error formula: ||x - x_tilde||_2^2 = sum_{j not in J} |c_j|^2
proj_diff_sq = np.linalg.norm(x_noisy - x_denoised) ** 2
discarded_energy = np.sum(np.abs(c_fft[~keep_mask]) ** 2)

rel_err_noisy = np.linalg.norm(x_noisy - x_clean) / np.linalg.norm(x_clean)
rel_err_denoised = np.linalg.norm(x_denoised - x_clean) / np.linalg.norm(x_clean)
kept_indices = np.where(keep_mask)[0]
kept_freqs = [int(k if k <= N // 2 else k - N) for k in kept_indices]

print(f"Retained {np.sum(keep_mask)} / {N} Fourier modes ({100 * np.sum(keep_mask) / N:.2f}%): frequencies = {kept_freqs} Hz")
print(f"Orthogonal projection identity: ||x_noisy - x_denoised||_2^2 = {proj_diff_sq:.4f}, "
      f"sum_{{j not in J}} |c_j|^2 = {discarded_energy:.4f}")
print(f"Relative 2-norm error vs. clean signal:")
print(f"  Noisy signal:    {100 * rel_err_noisy:.2f}%")
print(f"  Denoised signal: {100 * rel_err_denoised:.2f}%\n")

# ============================================================================
# 4. Complexity Benchmark: O(N^2) Dense F_N @ x vs. O(N log_2 N) np.fft.fft
# ============================================================================
sizes = [2**m for m in range(6, 14)]  # N = 64 .. 8192
times_dense = []
times_np_fft = []

# Warm up BLAS and FFT before timing
_ = F_N @ x_noisy
_ = np.fft.fft(x_noisy)

print(f"{'N':>6s} | {'Dense F_N @ x (ms)':>18s} | {'np.fft.fft (ms)':>15s} | {'Speedup':>10s}")
print("-" * 58)
for n_test in sizes:
    x_test = np.random.randn(n_test) + 0j
    F_test = build_dft_matrix(n_test)

    # Dense matrix-vector multiplication O(N^2)
    n_rep_dense = 20 if n_test <= 1024 else 5
    t0 = time.perf_counter()
    for _ in range(n_rep_dense):
        _ = F_test @ x_test
    t_dense = (time.perf_counter() - t0) * 1e3 / n_rep_dense
    times_dense.append(t_dense)

    # NumPy FFT O(N log N)
    t0 = time.perf_counter()
    for _ in range(50):
        _ = np.fft.fft(x_test)
    t_np = (time.perf_counter() - t0) * 1e3 / 50.0
    times_np_fft.append(t_np)

    print(f"{n_test:6d} | {t_dense:18.4f} | {t_np:15.4f} | {t_dense / t_np:9.1f}x")

# ============================================================================
# 5. Plot Time-Domain Signals, Fourier Spectrum, and Complexity Scaling
# ============================================================================
fig, axes = plt.subplots(2, 2, figsize=(13, 8))

# (a) Time domain: Clean vs. Noisy
ax = axes[0, 0]
ax.plot(t, x_noisy, color="lightgray", linewidth=1.0, label=f"Noisy signal (rel. err = {100*rel_err_noisy:.1f}%)")
ax.plot(t, x_clean, color="black", linewidth=1.8, label="Clean signal (5, 20, 60 Hz)")
ax.set_xlim(0, 0.5)
ax.set_xlabel("Time t (zoomed to [0, 0.5])")
ax.set_ylabel("Amplitude")
ax.set_title("1. Time Domain: Clean Signal Buried in Noise")
ax.legend(loc="upper right")
ax.grid(True, alpha=0.3)

# (b) Frequency domain: Unitary Fourier magnitude spectrum |c_k|
ax = axes[0, 1]
freqs_pos = np.arange(N // 2)
ax.plot(freqs_pos, np.abs(c_fft[: N // 2]), color="steelblue", linewidth=1.2, label=r"Unitary spectrum $|\hat{x}_k|$")
ax.axhline(threshold, color="crimson", linestyle="--", linewidth=1.5, label=rf"Threshold $\tau = {threshold:.2f}$")
ax.set_xlim(0, 120)
ax.set_xlabel("Frequency k (Hz)")
ax.set_ylabel(r"Magnitude $|\hat{x}_k| = |(\mathcal{F}_N \mathbf{x})_k|$")
ax.set_title("2. Frequency Domain: Sparse Signal Spikes vs. Flat Noise Floor")
ax.legend(loc="upper right")
ax.grid(True, alpha=0.3)

# (c) Time domain: Clean vs. Denoised via Fourier Projection
ax = axes[1, 0]
ax.plot(t, x_clean, color="black", linewidth=1.8, label="Clean signal")
ax.plot(
    t,
    x_denoised,
    color="crimson",
    linestyle="--",
    linewidth=1.6,
    label=f"Fourier projection ({np.sum(keep_mask)}/{N} modes, err = {100*rel_err_denoised:.1f}%)",
)
ax.set_xlim(0, 0.5)
ax.set_xlabel("Time t (zoomed to [0, 0.5])")
ax.set_ylabel("Amplitude")
ax.set_title(r"3. Orthogonal Projection $\tilde{\mathbf{x}} = \mathcal{F}_N^H \tilde{\mathbf{c}}$")
ax.legend(loc="upper right")
ax.grid(True, alpha=0.3)

# (d) Complexity scaling: O(N^2) vs. O(N log N)
ax = axes[1, 1]
sizes_arr = np.array(sizes, dtype=float)
ax.loglog(sizes_arr, times_dense, "o-", linewidth=2, label=r"Dense matvec $\mathbf{F}_N \mathbf{x}$ ($O(N^2)$)")
ax.loglog(sizes_arr, times_np_fft, "^-", linewidth=2, label=r"NumPy FFT ($O(N\log_2 N)$)")
ax.loglog(
    sizes_arr,
    times_dense[0] * (sizes_arr / sizes_arr[0]) ** 2,
    ":",
    color="gray",
    label=r"$O(N^2)$ reference slope",
)
ax.set_xlabel("Problem size N (log scale)")
ax.set_ylabel("Execution time (ms, log scale)")
ax.set_title(r"4. Complexity: Dense $\mathbf{F}_N\mathbf{x}$ ($O(N^2)$) vs. FFT ($O(N\log_2 N)$)")
ax.legend(loc="upper left")
ax.grid(True, which="both", alpha=0.3)

plt.suptitle("DFT & FFT in Numerical Linear Algebra: Unitary Projection Denoising and Complexity", fontsize=13)
plt.tight_layout()
plt.show()
