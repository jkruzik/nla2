import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

# Utility functions
def svd_compress(channel, k):
    """Compress a single channel using top-k singular values."""
    U, S, Vt = np.linalg.svd(channel, full_matrices=False)
    return np.dot(U[:, :k], np.dot(np.diag(S[:k]), Vt[:k, :])), len(S)

def reconstruct_image(img, k):
    """Reconstruct full image (handles grayscale and RGB)."""
    if img.ndim == 2:  # Grayscale
        recon, total_s = svd_compress(img, k)
        return recon, total_s * (img.shape[0] + img.shape[1] + 1)
    else:
        channels = []
        total_s = 0
        for i in range(3):
            recon, s_len = svd_compress(img[:, :, i], k)
            channels.append(recon)
            total_s += s_len * (img.shape[0] + img.shape[1] + 1)
        return np.stack(channels, axis=2).clip(0, 1), total_s

def compute_psnr(original, compressed):
    """Compute Peak Signal-to-Noise Ratio (PSNR)."""
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:
        return float('inf')
    return 10 * np.log10(1.0 / mse)

def compute_compression_ratio(img, k):
    """Compute theoretical compression ratio given k."""
    m, n = img.shape[:2]
    if img.ndim == 2:
        original_size = m * n
        compressed_size = k * (m + n + 1)
    else:
        original_size = 3 * m * n
        compressed_size = 3 * k * (m + n + 1)
    return original_size / compressed_size

# Load image
#image_path = "camera.png" # skimage.data.camera()
image_path = "astronaut.png" # skimage.data.astronaut()
img = imread(image_path).astype(float)
# Normalize to 0–1
if img.max() > 1:
    img /= 255.0

# Test different k values
k_values = [5, 10, 20, 40, 80, 120, 160, 200]
plt.figure(figsize=(15, 8))

for i, k in enumerate(k_values, 1):
    compressed_img, _ = reconstruct_image(img, k)
    psnr = compute_psnr(img, compressed_img)
    ratio = compute_compression_ratio(img, k)

    plt.subplot(3, 3, i)
    if img.ndim == 2:
        plt.imshow(compressed_img, cmap='gray')
    else:
        plt.imshow(compressed_img)
    plt.title(f'k={k}\nPSNR={psnr:.2f} dB\nRatio={ratio:.2f}x')
    plt.axis('off')

# Original image
plt.subplot(3, 3, 9)
if img.ndim == 2:
    plt.imshow(img, cmap='gray')
else:
    plt.imshow(img)
plt.title('Original')
plt.axis('off')

plt.suptitle('SVD Image Compression (with PSNR & Compression Ratio)', fontsize=16)
plt.tight_layout()
plt.show()

