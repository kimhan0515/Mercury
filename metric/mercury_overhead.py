import os
os.environ['HF_HOME'] = '/data/s1/jaehwan/hf_cache'

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from datasets import load_dataset
import time  # For measuring overhead

# Load dataset
dataset = load_dataset('Elfsong/Mercury')

# Initialize variables for overhead measurement
beyond_overhead = []
our_metric_overhead = []

# Process each task in the dataset
for instance in tqdm(dataset['eval'].to_list()):
    runtimes = []
    for solution in instance['solutions']:
        try:
            # Extract integer value before 'ms' and append to list
            runtime_str = solution['runtime'].split("ms")[0].strip()
            runtimes.append(int(runtime_str))
        except ValueError:
            print(f"Invalid runtime value: {solution['runtime']}")
    if len(runtimes) < 2:
        continue  # Skip tasks with less than 2 runtimes

    runtimes_sorted = sorted(runtimes)
    min_runtime = min(runtimes)
    max_runtime = max(runtimes)

    # Generate a random LLM runtime from the historical runtimes
    random_llm_runtime = np.random.choice(runtimes)

    # Measure Beyond Metric overhead
    start_time = time.time()
    beyond = max_runtime - random_llm_runtime
    beyond = min(beyond, 1)
    beyond = max(beyond, 0)
    beyond_percent = beyond / (max_runtime - min_runtime)
    end_time = time.time()
    beyond_overhead.append((end_time - start_time) * 1000)

    # Measure Our Metric overhead
    start_time = time.time()
    n = len(runtimes_sorted)
    cdf = 0.0  # Default CDF value
    # Linear interpolation for Non-uniform distributions
    for i in range(n - 1):
        if runtimes_sorted[i] <= random_llm_runtime <= runtimes_sorted[i + 1]:
            if runtimes_sorted[i + 1] - runtimes_sorted[i] == 0:
                cdf = (i + 1) / n
                break
            fraction = (random_llm_runtime - runtimes_sorted[i]) / (runtimes_sorted[i + 1] - runtimes_sorted[i])
            cdf = (i + fraction + 1) / n  # +1 for 1-based indexing
            break
    else:
        if random_llm_runtime > runtimes_sorted[-1]:  # Handle when runtime > max
            cdf = 1.0
        elif random_llm_runtime <= runtimes_sorted[0]:  # Handle when runtime <= min
            cdf = 0.0
    our_percent = 1 - cdf  # Higher is better
    end_time = time.time()
    our_metric_overhead.append((end_time - start_time) * 1000)

# Calculate average and total overhead in milliseconds
average_beyond_overhead = np.mean(beyond_overhead)  
average_our_metric_overhead = np.mean(our_metric_overhead)
total_beyond_overhead = np.sum(beyond_overhead)
total_our_metric_overhead = np.sum(our_metric_overhead)

# Print overhead results in milliseconds
print(f"Average Beyond Metric Overhead: {average_beyond_overhead:.6f} ms")
print(f"Average Our Metric Overhead: {average_our_metric_overhead:.6f} ms")
print(f"Total Beyond Metric Overhead: {total_beyond_overhead:.6f} ms")
print(f"Total Our Metric Overhead: {total_our_metric_overhead:.6f} ms")

# Visualize overhead comparison in milliseconds
plt.figure(figsize=(10, 8))

# Bar graph
bars = plt.bar(
    ["Beyond Metric", "Our Metric"], 
    [average_beyond_overhead, average_our_metric_overhead], 
    color=['green', 'blue'], 
    alpha=0.7
)

# Labels, title, and legend
plt.title("Overhead Comparison of Metrics", fontsize=16)
plt.ylabel("Average Overhead (ms)", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Save the figure
plt.savefig("figure/metric_overhead_comparison.png")