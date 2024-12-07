import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV into a DataFrame
file_path = "./data/deepseek-ai/deepseek-coder-1.3b-base_metric_score.csv"
data = pd.read_csv(file_path, header=None, names=["Pass@1", "Beyond Metric", "Our Metric", "Clustering"])

# Create DataFrame
df = pd.DataFrame(data, columns=["Pass@1", "Beyond Metric", "Our Metric", "Clustering"])

# Plot histograms for metrics
plt.figure(figsize=(12, 6))
plt.hist(df["Beyond Metric"], bins=50, alpha=0.5, label="Beyond Metric", range=(0, 1), color="green")  # Adjusted alpha
plt.hist(df["Our Metric"], bins=50, alpha=0.5, label="Our Metric", range=(0, 1), color="blue")  # Adjusted alpha
plt.hist(df["Clustering"], bins=50, alpha=0.5, label="Clustering", range=(0, 1), color="red")  # Adjusted alpha

plt.title("Robustness Comparison: Beyond Metric vs. Our Metric(+Clustering)", fontsize=16)
plt.xlabel("Metric Value (0-1)", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.legend(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("metric/figure/metric_robustness_comparison.png")