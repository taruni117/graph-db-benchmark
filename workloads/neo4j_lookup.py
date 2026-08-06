import time
import random
import statistics
import sys
import os

from neo4j import GraphDatabase

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def lookup(node_id):

    query = """
    MATCH (p:Person {id:$id})
    RETURN p.name
    """

    with driver.session() as session:
        session.run(
            query,
            id=node_id
        ).single()


times=[]


# Warmup
for _ in range(10):
    lookup(random.randint(1,20000))


# Benchmark
for _ in range(100):

    node=random.randint(1,20000)

    start=time.time()

    lookup(node)

    end=time.time()

    times.append(
        (end-start)*1000
    )


print("\nLookup Benchmark - Neo4j AuraDB\n")

print(
    "p50 :",
    round(statistics.median(times),2),
    "ms"
)

print(
    "p95 :",
    round(sorted(times)[94],2),
    "ms"
)


driver.close()