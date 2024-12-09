import numpy as np
import matplotlib.pyplot as plt

# Helper functions
# Helper functions
def beyond_metric(r, R):
    """Compute Beyond Metric Percentile."""
    P = (max(R) - r) / (max(R) - min(R))
    P = min(P, 1.0)
    P = max(P, 0.0)
    print("Beyond Metric Sensitivity:", r / (max(R) - min(R)))
    return P 

def cdf_with_interpolation(r, R_sorted):
    """Compute CDF with linear interpolation for Non-uniform distribution."""
    n = len(R_sorted)

    # Clip r to the range of R_sorted + epsilon to avoid matching the min/max values
    r = np.clip(r, R_sorted[0] + 1e-6, R_sorted[-1] - 1e-6)

    for i in range(n - 1):
        if R_sorted[i] <= r <= R_sorted[i + 1]:  # r is between two points
            if R_sorted[i + 1] - R_sorted[i] == 0:  # Handle zero division case
                return (i + 1) / n
            fraction = (r - R_sorted[i]) / (R_sorted[i + 1] - R_sorted[i])
            # print sensitivity regarding the error margins of r
            print("Our Metric Sensitivity:", r / (R_sorted[i + 1] - R_sorted[i]) / n)
            return (i + fraction + 1) / n
    # Handle edge cases outside the range
    if r > R_sorted[-1]:  # r is greater than max value
        return 1.0
    elif r < R_sorted[0]:  # r is less than min value
        return 0.0

def our_metric(r, R, is_non_uniform=False):
    """Compute Our Metric (1 - CDF-based Percentile)."""
    R_sorted = sorted(R)
    if is_non_uniform:  # Use linear interpolation for Non-uniform distributions
        cdf = cdf_with_interpolation(r, R_sorted)
    else:  # Uniform distribution: standard CDF calculation
        # cdf = sum(x <= r for x in R_sorted) / len(R_sorted)
        cdf = cdf_with_interpolation(r, R_sorted)
    
    return 1 - cdf

# Experiment setup
def simulate_metrics(R, r_base, margin_of_error, trials=1000, is_non_uniform=False):
    """Simulate Beyond and Our Metric with runtime variations."""
    beyond_results = []
    our_results = []
    for _ in range(trials):
        r = r_base + np.random.uniform(-margin_of_error, margin_of_error)
        beyond_results.append(beyond_metric(r, R))
        our_results.append(our_metric(r, R, is_non_uniform))
        print(f"R: {R} | Base: {r} | Margin: {margin_of_error}")
        print(f"Beyond: {beyond_results[-1]:.4f} | Our: {our_results[-1]:.4f}")
    return np.array(beyond_results), np.array(our_results)

# Uniform and Non-Uniform distributions
R_uniform = [10, 20, 30, 40, 50]
R_non_uniform = [5, 10, 10, 10, 40, 50]

# LLM-generated runtime and margin of error
r_base = 10  # Base runtime
margin_of_error = r_base * 0.01  # No margin of error for consistency

# Simulate results
# print("Uniform Distribution:")
beyond_uniform, our_uniform = simulate_metrics(R_uniform, r_base, margin_of_error)

# print("\nNon-Uniform Distribution:")
beyond_non_uniform, our_non_uniform = simulate_metrics(R_non_uniform, r_base, margin_of_error, is_non_uniform=True)

# Plot results
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
plt.suptitle("Robustness Comparison: Beyond vs. Our Metric", fontsize=16)

# Uniform distribution
axs[0, 0].hist(beyond_uniform, bins=20, alpha=0.7, label="Beyond Metric", color='green', range=(0.0, 1.0))
axs[0, 0].set_title("Uniform: Beyond", fontsize=14)
axs[0, 1].hist(our_uniform, bins=20, alpha=0.7, label="Our Metric", color='blue', range=(0.0, 1.0))
axs[0, 1].set_title("Uniform: Our Metric", fontsize=14)

# Non-Uniform distribution
axs[1, 0].hist(beyond_non_uniform, bins=20, alpha=0.7, label="Beyond Metric", color='green', range=(0.0, 1.0))
axs[1, 0].set_title("Non-Uniform: Beyond Metric", fontsize=14)
axs[1, 1].hist(our_non_uniform, bins=20, alpha=0.7, label="Our Metric", color='blue', range=(0.0, 1.0))
axs[1, 1].set_title("Non-Uniform: Our Metric (Interpolated)", fontsize=14)

# Formatting
for ax in axs.flat:
    ax.set_xlabel("Metric Value (0-1)", fontsize=14)
    ax.set_ylabel("Frequency (or Count)", fontsize=14)
    ax.legend(fontsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Save the plot
plt.savefig("figure/robustness.png")
