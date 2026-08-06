import json
import csv
import os


RESULTS_DIR = "results"


files = [
    "neo4j_mixed.json",
    "cognodb_mixed.json"
]


benchmark_data = []


for file in files:

    path = os.path.join(
        RESULTS_DIR,
        file
    )

    with open(path, "r") as f:
        data = json.load(f)

        benchmark_data.append(data)



# Print comparison

print("\nGraph Database Benchmark Comparison")
print("-----------------------------------")


for item in benchmark_data:

    print("\nDatabase:", item["database"])
    print("Workload:", item["workload"])
    print("QPS:", item["qps"])
    print("Average Latency:",
          item["average_latency_ms"],
          "ms")
    print("P95 Latency:",
          item["p95_latency_ms"],
          "ms")



# Save CSV

with open(
    "benchmark_results.csv",
    "w",
    newline=""
) as file:


    writer = csv.writer(file)


    writer.writerow(
        [
            "Database",
            "Workload",
            "Concurrency",
            "Queries",
            "Time Seconds",
            "QPS",
            "Average Latency ms",
            "P95 Latency ms"
        ]
    )


    for item in benchmark_data:

        writer.writerow(
            [
                item["database"],
                item["workload"],
                item["concurrency"],
                item["total_queries"],
                item["time_seconds"],
                item["qps"],
                item["average_latency_ms"],
                item["p95_latency_ms"]
            ]
        )


print(
    "\nSaved: benchmark_results.csv"
)