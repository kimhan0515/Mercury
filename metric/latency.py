import numpy as np
import matplotlib.pyplot as plt
import time

# Helper functions
def beyond_metric(r, R):
    """Compute Beyond Metric Percentile."""
    return (max(R) - r) / (max(R) - min(R))

def cdf_with_interpolation(r, R_sorted):
    """Compute CDF with linear interpolation for Non-uniform distribution."""
    n = len(R_sorted)
    for i in range(n - 1):
        if R_sorted[i] <= r <= R_sorted[i + 1]:  # r is between two points
            fraction = (r - R_sorted[i]) / (R_sorted[i + 1] - R_sorted[i])
            return (i + fraction + 1) / n  # +1 to account for 1-based indexing
        else:
            return 1.0 if r > R_sorted[-1] else 0.0  # Handle edge cases

def our_metric(r, R, is_non_uniform=False):
    """Compute Our Metric (1 - CDF-based Percentile)."""
    R_sorted = sorted(R)
    if is_non_uniform:  # Use linear interpolation for Non-uniform distributions
        cdf = cdf_with_interpolation(r, R_sorted)
    else:  # Uniform distribution: standard CDF calculation
        cdf = sum(x <= r for x in R_sorted) / len(R_sorted)
    
    return 1 - cdf

# Experiment setup
def simulate_metrics(R, r_base, margin_of_error, trials=1000, is_non_uniform=False):
    """Simulate Beyond and Our Metric with runtime variations."""
    beyond_results = []
    our_results = []
    for _ in range(trials):
        r = r_base + np.random.uniform(-margin_of_error, margin_of_error)
        beyond_start = time.time()
        beyond_results.append(beyond_metric(r, R))
        beyond_end = time.time()
        beyond_latency.append(beyond_end - beyond_start)
        our_start = time.time()
        our_results.append(our_metric(r, R, is_non_uniform))
        our_end = time.time()
        our_latency.append(our_end - our_start)
        # print(f"R: {R} | Base: {r_base} | Margin: {margin_of_error}")
        # print(f"Beyond: {beyond_results[-1]:.4f} | Our: {our_results[-1]:.4f}")
    return np.array(beyond_results), np.array(our_results)

if __name__ == "__main__":
	# Uniform and Non-Uniform distributions
	R_uniform = [1, 2, 3, 4, 5]
	R_non_uniform = [1, 1, 1, 4, 5]

	# LLM-generated runtime and margin of error
	r_base = 3.5  # Base runtime
	margin_of_error = r_base * 0.0  # No margin of error for consistency

	# Latency
	beyond_latency = []
	our_latency = []

	# Simulate results
	# print("Uniform Distribution:")
	beyond_uniform, our_uniform = simulate_metrics(R_uniform, r_base, margin_of_error)

	# print("\nNon-Uniform Distribution:")
	beyond_non_uniform, our_non_uniform = simulate_metrics(R_non_uniform, r_base, margin_of_error, is_non_uniform=True)

	# Average Latency
	beyond_uniform_latency = sum(beyond_latency) / len(beyond_latency)
	our_uniform_latency = sum(our_latency) / len(our_latency)
	print(f"Average Latency for Beyond Metric (Uniform): {beyond_uniform_latency:.6f}")

	# Total Sum of Latency
	beyond_uniform_latency = sum(beyond_latency)
	our_uniform_latency = sum(our_latency)
	print(f"Total Sum of Latency for Beyond Metric (Uniform): {beyond_uniform_latency:.6f}")

