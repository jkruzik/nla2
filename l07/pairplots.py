import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

# Create DataFrame for easy plotting
df = pd.DataFrame(X, columns=feature_names)
df['species'] = [target_names[i] for i in y]

# Pairplot (scatterplot matrix)
sns.pairplot(df, hue='species', diag_kind='kde', corner=True)
plt.suptitle("Pairwise Feature Relationships in Iris Dataset", y=1.02)
plt.show()

# Correlation heatmap
corr = df.iloc[:, :-1].corr()
plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title("Feature Correlation Heatmap (Iris Dataset)")
plt.show()

