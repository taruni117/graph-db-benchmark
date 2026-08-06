import os
import sys
import time
import random
import statistics
import json

from neo4j import GraphDatabase

# Import config.py
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


def percentile(data, p):
    data = sorted(data)
    k = int((len(data) - 1) * p / 100)
    return data[k]


def get_random_ids():
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Person)
            RETURN p.id AS id
            ORDER BY rand()
            LIMIT 100
        """)
        return [r["id"] for r in result]


ids = get_random_ids()

times = []

with driver.session() as session:

    for node_id in ids:

        start = time.perf_counter()

        session.run("""
            MATCH (p:Person {id:$id})
            RETURN p
        """, id=node_id).consume()

        end = time.perf_counter()

        times.append((end - start) * 1000)

p50 = percentile(times, 50)
p95 = percentile(times, 95)

print("\nLookup Benchmark\n")
print(f"p50 : {p50:.2f} ms")
print(f"p95 : {p95:.2f} ms")

os.makedirs("results", exist_ok=True)

with open("results/cognodb_lookup.json", "w") as f:
    json.dump({
        "database": "CognoDB",
        "lookup": {
            "p50": p50,
            "p95": p95
        }
    }, f, indent=4)

driver.close()