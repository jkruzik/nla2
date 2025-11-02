import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

# Load a dataset (Iris)
iris = datasets.load_iris()
X_raw = iris.data
y = iris.target
target_names = iris.target_names

# Standardize the data (zero mean, unit variance)
X_mean = X_raw - np.mean(X_raw, axis=0)
X_std = X_mean / np.std(X_mean, axis=0)
X = X_mean

#X = X_std

# Compute SVD
U, S, Vt = np.linalg.svd(X, full_matrices=False)
print(Vt[:,:2])

# Project data onto principal directions = principal components
# XV = US
X_pca = U[:, :2] * S[:2]

# Explained variance ratio
explained_variance = (S ** 2) / (len(X_std) - 1)
explained_variance_ratio = explained_variance / explained_variance.sum()

print("Explained variance ratio:", explained_variance_ratio[:2])
print("Total variance explained by 2 components:", explained_variance_ratio[:2].sum())

# Plot first component
plt.figure(figsize=(8, 6))
colors = ['navy', 'turquoise', 'darkorange']
for color, i, target_name in zip(colors, [0, 1, 2], target_names):
    plt.scatter(X_pca[y == i, 0], np.zeros_like(X_pca[y == i, 0]),color=color, lw=2, label=target_name)

plt.xlabel("Principal Component 1")
plt.legend()
plt.grid(True)
plt.show()

# Plot first and second component
plt.figure(figsize=(8, 6))
for color, i, target_name in zip(colors, [0, 1, 2], target_names):
    plt.scatter(X_pca[y == i, 0], X_pca[y == i, 1], color=color, lw=2, label=target_name)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()
plt.grid(True)
plt.show()

