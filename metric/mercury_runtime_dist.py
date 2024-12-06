import os
os.environ['HF_HOME'] = '/data/s1/jaehwan/hf_cache'

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from datasets import load_dataset
from scipy.stats import chisquare

# Load dataset
dataset = load_dataset('Elfsong/Mercury')

def is_uniform_distribution(data, threshold=0.25):
    """
    Check if a distribution is uniform based on the coefficient of variation (CV).
    A CV below the threshold indicates uniformity.
    """
    if len(data) <= 1:
        return False  # Cannot classify if only one or zero runtime values
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)  # Sample standard deviation (Bessel's correction)
    cv = std_dev / mean  # Coefficient of Variation
    return cv < threshold

# def is_uniform_chisquare(data):
#     observed_counts = [data.count(x) for x in set(data)]
#     expected_counts = [len(data) / len(set(data))] * len(set(data))
#     chi2, p_value = chisquare(observed_counts, f_exp=expected_counts)
#     return p_value > 0.05  # p-value > 0.05 means likely uniform

def is_uniform_chisquare(data, cov_threshold=0.2325):
    # Calculate observed and expected counts
    observed_counts = [data.count(x) for x in set(data)]
    expected_counts = [len(data) / len(set(data))] * len(set(data))
    
    # Perform Chi-Square test
    chi2, p_value = chisquare(observed_counts, f_exp=expected_counts)
    
    # Calculate CoV
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1) if len(data) > 1 else 0  # Avoid division by zero
    cov = std_dev / mean if mean != 0 else float('inf')  # Avoid division by zero
    
    # Combine Chi-Square and CoV results
    return p_value > 0.05 and cov < cov_threshold  # Both conditions must be satisfied

# Collect distribution stats
all_runtimes = []
task_distributions = []
uniform_task_ids = []
non_uniform_task_ids = []

for task_id, instance in enumerate(tqdm(dataset['eval'].to_list())):
    runtimes = []
    for solution in instance['solutions']:
        try:
            # Extract integer value before 'ms' and append to list
            runtime_str = solution['runtime'].split("ms")[0].strip()
            runtimes.append(int(runtime_str))
        except ValueError:
            print(f"Invalid runtime value: {solution['runtime']}")
    task_distributions.append(runtimes)
    all_runtimes.extend(runtimes)
    
    # Classify each task as uniform or non-uniform
    if is_uniform_chisquare(runtimes):
        uniform_task_ids.append(task_id)
        print(f"Task {task_id} is a uniform distribution.")
    else:
        non_uniform_task_ids.append(task_id)

print(f"Number of uniform tasks: {len(uniform_task_ids)}")
print(f"Number of non-uniform tasks: {len(non_uniform_task_ids)}")

# Plot global histogram
plt.figure(figsize=(10, 6))
plt.hist(all_runtimes, bins=50, alpha=0.7, color='blue')
plt.title("Overall Runtime Distribution (All Tasks)", fontsize=16)
plt.xlabel("Runtime (ms)", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.grid()
plt.savefig("figure/runtime_distribution.png")

# Plot selected tasks for comparison
fig, axs = plt.subplots(2, 3, figsize=(15, 10))
plt.suptitle("Runtime Distributions", fontsize=24)
sample_tasks = [9, 84, 155, 204, 208, 212]  # Sample 6 tasks for visualization

for i, task_id in enumerate(sample_tasks):
    ax = axs[i // 3, i % 3]
    ax.hist(task_distributions[task_id], bins=10, alpha=0.7, color='green')
    ax.set_title(f"Task {task_id}", fontsize=20)
    ax.set_xlabel("Runtime (ms)", fontsize=18)
    ax.set_ylabel("Frequency", fontsize=18)
    ax.grid()

plt.tight_layout()
plt.savefig("figure/task_runtime_distribution.png")

# Boxplot for all tasks
plt.figure(figsize=(12, 8))
plt.boxplot(task_distributions, showfliers=False, vert=True)
plt.title("Task-wise Runtime Distribution", fontsize=16)
plt.xlabel("Task ID", fontsize=14)
plt.ylabel("Runtime (ms)", fontsize=14)
plt.savefig("figure/task_runtime_boxplot.png")

# Save uniform and non-uniform task IDs for reference
# with open("uniform_tasks.txt", "w") as uniform_file:
#     uniform_file.write("\n".join(map(str, uniform_task_ids)))

# with open("non_uniform_tasks.txt", "w") as non_uniform_file:
#     non_uniform_file.write("\n".join(map(str, non_uniform_task_ids)))
