import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread


def build_single_level_haar_matrix(n):
    """
    Build the single-level n x n orthogonal Haar matrix W_tilde_n = [H_{n/2}; G_{n/2}]
    from Section 5.3.2 of the notes (2 nonzeros per row):
      - Top n/2 rows (H_{n/2}):    local averages    (x_{2k} + x_{2k+1}) / sqrt(2)
      - Bottom n/2 rows (G_{n/2}): local differences (x_{2k} - x_{2k+1}) / sqrt(2)
    """
    if n % 2 != 0:
        raise ValueError("Matrix dimension n must be even.")
    half = n // 2
    W_tilde = np.zeros((n, n), dtype=float)
    s = 1.0 / np.sqrt(2.0)
    for k in range(half):
        # Low-pass (approximation / scaling) row k
        W_tilde[k, 2 * k] = s
        W_tilde[k, 2 * k + 1] = s
        # High-pass (detail / wavelet) row half + k
        W_tilde[half + k, 2 * k] = s
        W_tilde[half + k, 2 * k + 1] = -s
    return W_tilde


def mallat_haar_2d(img, levels):
    """
    2D Mallat pyramid algorithm using the single-level Haar matrix W_tilde_n:
    At each level l = 1..levels, apply the separable 2D orthogonal transform
        Y_n = W_tilde_n @ X_n @ W_tilde_n^T = [[LL, LH], [HL, HH]]
    only to the current top-left approximation block X_n of size n = N / 2^{l-1}.
    """
    Y = img.astype(float).copy()
    n = Y.shape[0]
    for _ in range(levels):
        W_tilde = build_single_level_haar_matrix(n)
        Y[:n, :n] = W_tilde @ Y[:n, :n] @ W_tilde.T
        n //= 2
    return Y


def imallat_haar_2d(coeffs, levels):
    """
    Inverse 2D Mallat pyramid algorithm:
    Iterate from coarsest level l = levels down to 1, applying the transposed
    orthogonal transform X_n = W_tilde_n^T @ Y_n @ W_tilde_n.
    """
    X = coeffs.astype(float).copy()
    n = X.shape[0] // (2 ** (levels - 1))
    for _ in range(levels):
        W_tilde = build_single_level_haar_matrix(n)
        X[:n, :n] = W_tilde.T @ X[:n, :n] @ W_tilde
        n *= 2
    return X


def compress_wavelet_coeffs(coeffs, keep_ratio):
    """Keep only the top `keep_ratio` fraction of wavelet coefficients by magnitude."""
    total_coeffs = coeffs.size
    k_keep = max(1, int(round(keep_ratio * total_coeffs)))
    flat_abs = np.abs(coeffs).ravel()
    # Threshold tau is the k_keep-th largest magnitude
    threshold = np.partition(flat_abs, -k_keep)[-k_keep]
    mask = np.abs(coeffs) >= threshold
    compressed = np.where(mask, coeffs, 0.0)
    return compressed, mask, threshold


def compute_psnr(original, compressed):
    """Compute Peak Signal-to-Noise Ratio (PSNR) in dB for images in [0, 1]."""
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:
        return float("inf")
    return 10.0 * np.log10(1.0 / mse)


# ============================================================================
# 1. Load grayscale image (512 x 512) and compute L-level Mallat Haar pyramid
# ============================================================================
image_path = "../l06/camera.png"
img = imread(image_path).astype(float)
if img.max() > 1.0:
    img /= 255.0
if img.ndim == 3:
    img = 0.2989 * img[:, :, 0] + 0.5870 * img[:, :, 1] + 0.1140 * img[:, :, 2]

N = img.shape[0]
# TODO vary number of Mallat pyramid levels (1 .. int(np.log2(N)))
levels = 3

W_tilde_N = build_single_level_haar_matrix(N)
orth_err = np.linalg.norm(W_tilde_N.T @ W_tilde_N - np.eye(N), ord=2)

coeffs = mallat_haar_2d(img, levels=levels)
img_reconstructed = imallat_haar_2d(coeffs, levels=levels)
recon_err = np.linalg.norm(img - img_reconstructed, ord="fro")

print(f"Image shape: {img.shape} (N = {N} = 2^{int(np.log2(N))}), Mallat pyramid levels L = {levels}")
print(f"Single-level Haar matrix orthogonality ||W_tilde^T W_tilde - I||_2 = {orth_err:.2e}")
print(f"Parseval's identity (Frobenius norm): ||X||_F^2 = {np.linalg.norm(img, 'fro')**2:.4f}, "
      f"||Y||_F^2 = {np.linalg.norm(coeffs, 'fro')**2:.4f}")
print(f"Perfect reconstruction error ||X - W^T Y W||_F = {recon_err:.2e}\n")

# ============================================================================
# 2. Plot Original Image, L-Level Mallat Wavelet Pyramid, and Sparsity Profile
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))

axes[0].imshow(img, cmap="gray", vmin=0, vmax=1)
axes[0].set_title(f"Original Image ({N}x{N})")
axes[0].axis("off")

# Visualize Mallat pyramid (log-scaled magnitudes for visibility of detail subbands)
pyramid_vis = np.log1p(np.abs(coeffs))
axes[1].imshow(pyramid_vis, cmap="gray")
n_sub = N
for _ in range(levels):
    half = n_sub // 2
    axes[1].plot([0, n_sub], [half, half], color="gold", linewidth=1.0)
    axes[1].plot([half, half], [0, n_sub], color="gold", linewidth=1.0)
    n_sub = half
axes[1].set_xlim(0, N)
axes[1].set_ylim(N, 0)
axes[1].set_title(f"{levels}-Level Mallat Pyramid (log |Y|)\nCoarse LL_{levels} ({N // 2**levels}x{N // 2**levels}) + Detail Subbands")
axes[1].axis("off")

# Sorted wavelet coefficient decay (energy compaction)
sorted_abs = np.sort(np.abs(coeffs).ravel())[::-1]
cum_energy = np.cumsum(sorted_abs**2) / np.sum(sorted_abs**2)
pct_coeffs = 100.0 * np.arange(1, len(sorted_abs) + 1) / len(sorted_abs)
axes[2].plot(pct_coeffs, 100.0 * cum_energy, color="steelblue", linewidth=2)
axes[2].axvline(5.0, color="crimson", linestyle="--", label=f"Top 5% coeffs -> {100*cum_energy[int(0.05*len(sorted_abs))]:.2f}% energy")
axes[2].set_xlim(0, 25)
axes[2].set_ylim(80, 100.2)
axes[2].set_xlabel("Percentage of largest wavelet coefficients kept (%)")
axes[2].set_ylabel("Captured Frobenius energy ||Y_kept||_F^2 / ||X||_F^2 (%)")
axes[2].set_title("Wavelet Energy Compaction")
axes[2].legend(loc="lower right")
axes[2].grid(True, alpha=0.3)

plt.suptitle("2D Mallat Haar Wavelet Pyramid Decomposition", fontsize=13)
plt.tight_layout()

# ============================================================================
# 3. Compress Image at Various Retention Ratios and Verify Parseval Error
# ============================================================================
keep_ratios = [0.50, 0.20, 0.10, 0.05, 0.02, 0.01]  # 50% down to 1% kept
plt.figure(figsize=(14, 8))

print(f"{'Kept (%)':>9s} | {'Comp. Ratio':>11s} | {'Threshold tau':>13s} | {'PSNR (dB)':>10s} | {'||X - X_tilde||_F^2':>19s} | {'Discarded sum Y_ij^2':>20s}")
print("-" * 96)

for idx, ratio in enumerate(keep_ratios, start=1):
    coeffs_thresh, mask, tau = compress_wavelet_coeffs(coeffs, ratio)
    img_comp = imallat_haar_2d(coeffs_thresh, levels=levels)

    # Check exact orthogonal thresholding error ||X - X_tilde||_F^2 = sum_{(i,j) not in J} Y_{ij}^2
    err_fro_sq = np.linalg.norm(img - img_comp, ord="fro") ** 2
    discarded_sq = np.sum(coeffs[~mask] ** 2)

    img_comp_clipped = np.clip(img_comp, 0.0, 1.0)
    psnr = compute_psnr(img, img_comp_clipped)
    comp_ratio = 1.0 / ratio

    print(f"{100 * ratio:8.1f}% | {comp_ratio:10.1f}x | {tau:13.5f} | {psnr:10.2f} | {err_fro_sq:19.4f} | {discarded_sq:20.4f}")

    plt.subplot(2, 3, idx)
    plt.imshow(img_comp_clipped, cmap="gray", vmin=0, vmax=1)
    plt.title(f"Kept {100*ratio:.0f}% (Ratio {comp_ratio:.0f}x)\nPSNR = {psnr:.2f} dB")
    plt.axis("off")

plt.suptitle(f"Haar Wavelet Image Compression ({levels}-Level Mallat Pyramid)", fontsize=14)
plt.tight_layout()
plt.show()
