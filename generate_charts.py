import csv
import os
import matplotlib.pyplot as plt


databases = []
qps = []
latency = []
p95 = []


with open("benchmark_results.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:
        databases.append(row["Database"])
        qps.append(float(row["QPS"]))
        latency.append(float(row["Average Latency ms"]))
        p95.append(float(row["P95 Latency ms"]))


os.makedirs("charts", exist_ok=True)


# QPS Comparison

plt.figure(figsize=(8,5))

plt.bar(databases, qps)

plt.title("Graph Database Throughput Comparison")

plt.ylabel("Queries Per Second")

plt.savefig(
    "charts/qps_comparison.png",
    bbox_inches="tight"
)

plt.close()



# Average Latency Comparison

plt.figure(figsize=(8,5))

plt.bar(databases, latency)

plt.title("Average Query Latency Comparison")

plt.ylabel("Latency (ms)")

plt.savefig(
    "charts/latency_comparison.png",
    bbox_inches="tight"
)

plt.close()



# P95 Latency Comparison

plt.figure(figsize=(8,5))

plt.bar(databases, p95)

plt.title("P95 Latency Comparison")

plt.ylabel("Latency (ms)")

plt.savefig(
    "charts/p95_latency_comparison.png",
    bbox_inches="tight"
)

plt.close()


print("Charts generated successfully")