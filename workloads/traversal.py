import os
import sys
import time
import random
import statistics

from neo4j import GraphDatabase

# Import config.py from project root
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


def get_random_ids():
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Person)
            RETURN p.id AS id
            ORDER BY rand()
            LIMIT 100
        """)
        return [r["id"] for r in result]


def benchmark(query, ids):

    times = []

    with driver.session() as session:

        for node_id in ids:

            start = time.perf_counter()

            session.run(query, id=node_id).consume()

            end = time.perf_counter()

            times.append((end - start) * 1000)

    p50 = statistics.median(times)

    p95 = statistics.quantiles(times, n=100)[94]

    return p50, p95


ids = get_random_ids()

queries = {
    "1-hop":
    """
    MATCH (p:Person {id:$id})-[:KNOWS]->()
    RETURN count(*)
    """,

    "2-hop":
    """
    MATCH (p:Person {id:$id})-[:KNOWS]->()-[:KNOWS]->()
    RETURN count(*)
    """,

    "3-hop":
    """
    MATCH (p:Person {id:$id})-[:KNOWS]->()-[:KNOWS]->()-[:KNOWS]->()
    RETURN count(*)
    """
}

print("\nTraversal Benchmark\n")

for name, query in queries.items():

    p50, p95 = benchmark(query, ids)

    print(f"{name}")
    print(f"   p50 : {p50:.2f} ms")
    print(f"   p95 : {p95:.2f} ms\n")

driver.close()