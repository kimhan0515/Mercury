# Given R_sorted and LLM-generated runtime
R_sorted = [
    0.0007169246673583984, 0.0007491111755371094, 0.0007586479187011719,
    0.0007596015930175781, 0.0007789134979248047, 0.0009777545928955078,
    0.0009808540344238281, 0.0009877681732177734, 0.0009930133819580078,
    0.0009937286376953125, 0.0009946823120117188, 0.0010161399841308594,
    0.001024484634399414, 0.0010271072387695312, 0.0010330677032470703,
    0.0010497570037841797, 0.0011224746704101562, 0.0011234283447265625,
    0.0011944770812988281, 0.0012509822845458984
]
runtime = 0.0010554790496826172

# test Clustering
cluster_sorted = []
current_cluster = [R_sorted[0]]

cluster_threshold = (R_sorted[-1] - R_sorted[0]) / 100
for i in range(len(R_sorted) - 1):
    current_cluster.append(R_sorted[i])
    if R_sorted[i+1] - R_sorted[i] > cluster_threshold:
        if len(current_cluster) != 0:
            cluster_sorted.append(sum(current_cluster)/len(current_cluster))
            current_cluster = []
    current_cluster.append(R_sorted[i+1])

cluster_sorted.append(sum(current_cluster) / len(current_cluster))

print(cluster_sorted)

# Beyond Metric Sensitivity
beyond_sensitivity = 1 / (max(R_sorted) - min(R_sorted))

# Our Metric Sensitivity
n = len(R_sorted)
our_sensitivity = 0
for i in range(len(R_sorted) - 1):
    if R_sorted[i] <= runtime <= R_sorted[i + 1]:
        interval = R_sorted[i + 1] - R_sorted[i]
        if interval != 0:
            our_sensitivity = 1 / (interval * n)
        break

# Our Metric + Cluster Sensitivity
n = len(cluster_sorted)
cluster_sensitivity = 0
for i in range(len(cluster_sorted) - 1):
    if cluster_sorted[i] <= runtime <= cluster_sorted[i + 1]:
        interval = cluster_sorted[i + 1] - cluster_sorted[i]
        if interval != 0:
            cluster_sensitivity = 1 / (interval * n)
        break

print(f"Beyond Metric Sensitivity: {beyond_sensitivity:.4f}")
print(f"Our Metric Sensitivity: {our_sensitivity:.4f}")
print(f"Cluster Sensitivity: {our_sensitivity:.4f}")