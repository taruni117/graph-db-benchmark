import os
import sys
import time
import statistics
import json

from neo4j import GraphDatabase

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import (
    COGNODB_URI,
    COGNODB_USER,
    COGNODB_PASSWORD
)

driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USER, COGNODB_PASSWORD)
)

ITERATIONS = 100

times = []

query = """
MATCH (p:Person)
RETURN count(p) AS total
"""

with driver.session() as session:

    # Warm-up
    session.run(query).consume()

    for _ in range(ITERATIONS):

        start = time.perf_counter()

        session.run(query).consume()

        end = time.perf_counter()

        times.append((end - start) * 1000)

times.sort()

p50 = statistics.median(times)
p95 = times[int(0.95 * len(times)) - 1]

print("\nAggregation Benchmark\n")
print(f"p50 : {p50:.2f} ms")
print(f"p95 : {p95:.2f} ms")

os.makedirs("results", exist_ok=True)

with open("results/cognodb_aggregation.json", "w") as f:
    json.dump(
        {
            "database": "CognoDB",
            "aggregation": {
                "p50": p50,
                "p95": p95
            }
        },
        f,
        indent=4
    )

driver.close()