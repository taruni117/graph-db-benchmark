import json
import time
import random
import concurrent.futures
import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# Import CognoDB configuration
from config import COGNODB_URI


# -----------------------------
# CognoDB Connection Placeholder
# -----------------------------
# Update this according to CognoDB SDK/API
# after checking your existing lookup.py and aggregation.py files


def read_query():

    start = time.time()

    # TODO:
    # Add CognoDB read query here
    #
    # Example:
    # client.query(...)

    time.sleep(0.01)

    latency = (time.time() - start) * 1000

    return latency



def write_query():

    start = time.time()

    # TODO:
    # Add CognoDB write query here

    time.sleep(0.01)

    latency = (time.time() - start) * 1000

    return latency



def worker():

    if random.random() < 0.8:
        return read_query()

    else:
        return write_query()



print("\nMixed Workload - CognoDB")
print("-------------------------")
print("Concurrency: 10 clients")
print("Read/Write mix: 80/20")


TOTAL_QUERIES = 1000
CONCURRENCY = 10


latencies = []


start = time.time()


with concurrent.futures.ThreadPoolExecutor(
    max_workers=CONCURRENCY
) as executor:

    futures = [
        executor.submit(worker)
        for _ in range(TOTAL_QUERIES)
    ]


    for future in futures:
        latencies.append(
            future.result()
        )



elapsed = time.time() - start


qps = TOTAL_QUERIES / elapsed


avg_latency = sum(latencies) / len(latencies)


p95_latency = sorted(latencies)[
    int(len(latencies) * 0.95)
]


print("\nResults")
print("----------------")
print("Total Queries :", TOTAL_QUERIES)
print("Time:", round(elapsed,2), "sec")
print("QPS:", round(qps,2))
print("Average Latency:", round(avg_latency,2), "ms")
print("P95 Latency:", round(p95_latency,2), "ms")



# Save results

os.makedirs(
    "results",
    exist_ok=True
)


result = {

    "database": "CognoDB",

    "workload": "Mixed",

    "read_write_ratio": "80/20",

    "concurrency": CONCURRENCY,

    "total_queries": TOTAL_QUERIES,

    "time_seconds": round(elapsed,2),

    "qps": round(qps,2),

    "average_latency_ms": round(avg_latency,2),

    "p95_latency_ms": round(p95_latency,2)

}


with open(
    "results/cognodb_mixed.json",
    "w"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )


print("\nSaved: results/cognodb_mixed.json")