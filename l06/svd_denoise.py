import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread


def to_grayscale(img):
    """Convert image to grayscale float array in [0, 1]."""
    img = img.astype(float)
    if img.max() > 1.0:
        img /= 255.0
    if img.ndim == 3:
        img = 0.2989 * img[:, :, 0] + 0.5870 * img[:, :, 1] + 0.1140 * img[:, :, 2]
    return img


def svd_reconstruct(U, S, Vt, k):
    """Reconstruct rank-k approximation A_k = U_k @ diag(S_k) @ Vt_k."""
    recon = (U[:, :k] * S[:k]) @ Vt[:k, :]
    return np.clip(recon, 0.0, 1.0)


def compute_psnr(clean, estimate):
    """Compute Peak Signal-to-Noise Ratio (PSNR) in dB relative to clean image."""
    mse = np.mean((clean - estimate) ** 2)
    if mse == 0:
        return float("inf")
    return 10.0 * np.log10(1.0 / mse)


# 1. Load clean image and add Gaussian noise
np.random.seed(42)
image_path = "plaid_pattern.jpg"  # Low-rank structured image low res of https://commons.wikimedia.org/wiki/File:Tartan_Plaid_-_Macro_(49852164907).jpg
#image_path = "camera.png"       # Natural grayscale image
img_clean = to_grayscale(imread(image_path))

noise_std = 0.15
noise = np.random.normal(0.0, noise_std, img_clean.shape)
img_noisy = np.clip(img_clean + noise, 0.0, 1.0)

# 2. Compute SVD of noisy image (and clean/noise for spectrum comparison)
U, S_noisy, Vt = np.linalg.svd(img_noisy, full_matrices=False)
S_clean = np.linalg.svd(img_clean, compute_uv=False)
S_noise = np.linalg.svd(noise, compute_uv=False)

max_rank = len(S_noisy)
psnr_noisy = compute_psnr(img_clean, img_noisy)
print(f"Image shape: {img_clean.shape} (max rank r = {max_rank})")
print(f"Noisy image PSNR: {psnr_noisy:.2f} dB\n")

# 3. Evaluate PSNR across all possible truncation ranks k = 1..r
all_k = np.arange(1, max_rank + 1)
psnr_curve = [compute_psnr(img_clean, svd_reconstruct(U, S_noisy, Vt, k)) for k in all_k]
best_k = int(all_k[np.argmax(psnr_curve)])
best_psnr = max(psnr_curve)
print(f"Optimal rank k* = {best_k} with PSNR = {best_psnr:.2f} dB (+{best_psnr - psnr_noisy:.2f} dB gain)\n")

# 4. Plot visual comparison for selected ranks k
k_values = [1, 3, best_k, 25, 60, 120]
plt.figure(figsize=(14, 7))

plt.subplot(2, 4, 1)
plt.imshow(img_clean, cmap="gray", vmin=0, vmax=1)
plt.title("Original (Clean)")
plt.axis("off")

plt.subplot(2, 4, 2)
plt.imshow(img_noisy, cmap="gray", vmin=0, vmax=1)
plt.title(f"Noisy (sigma={noise_std})\nPSNR={psnr_noisy:.2f} dB")
plt.axis("off")

for idx, k in enumerate(k_values, start=3):
    img_denoised = svd_reconstruct(U, S_noisy, Vt, k)
    psnr_k = compute_psnr(img_clean, img_denoised)
    print(f"Rank k = {k:3d} | PSNR = {psnr_k:.2f} dB")

    plt.subplot(2, 4, idx)
    plt.imshow(img_denoised, cmap="gray", vmin=0, vmax=1)
    label = f"k={k} (Optimal)" if k == best_k else f"k={k}"
    plt.title(f"{label}\nPSNR={psnr_k:.2f} dB")
    plt.axis("off")

plt.suptitle("SVD Image Denoising: Low-Rank Signal vs. High-Rank Noise", fontsize=14)
plt.tight_layout()

# 5. Plot singular value spectrum and PSNR vs. rank k
plt.figure(figsize=(12, 4.5))

plt.subplot(1, 2, 1)
plt.semilogy(all_k, S_clean, label="Original image (signal)", linewidth=2)
plt.semilogy(all_k, S_noisy, label="Noisy image", linewidth=2)
plt.semilogy(all_k, S_noise, "--", label="Pure Gaussian noise", alpha=0.8)
plt.axvline(best_k, color="red", linestyle=":", label=f"Optimal cutoff k*={best_k}")
plt.xlabel("Singular value index i")
plt.ylabel("Singular value sigma_i (log scale)")
plt.title("Singular Value Spectrum (Signal vs. Noise Floor)")
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(all_k, psnr_curve, linewidth=2, label="Denoised PSNR(k)")
plt.axhline(psnr_noisy, color="gray", linestyle="--", label=f"Noisy baseline ({psnr_noisy:.2f} dB)")
plt.axvline(best_k, color="red", linestyle=":", label=f"Optimal k*={best_k} ({best_psnr:.2f} dB)")
plt.xlabel("Truncation rank k")
plt.ylabel("PSNR (dB)")
plt.title("Denoising Quality (PSNR) vs. Rank k")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
