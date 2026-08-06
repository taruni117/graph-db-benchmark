import time
import random
import statistics
from neo4j import GraphDatabase
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def run_query(depth, node_id):

    if depth == 1:
        query = """
        MATCH (a:Person {id:$id})-[:FRIEND]->(b)
        RETURN count(b)
        """

    elif depth == 2:
        query = """
        MATCH (a:Person {id:$id})
              -[:FRIEND]->()
              -[:FRIEND]->(b)
        RETURN count(b)
        """

    else:
        query = """
        MATCH (a:Person {id:$id})
              -[:FRIEND]->()
              -[:FRIEND]->()
              -[:FRIEND]->(b)
        RETURN count(b)
        """

    with driver.session() as session:
        session.run(query, id=node_id).single()


def benchmark(depth):

    times = []

    # warmup
    for _ in range(10):
        run_query(depth, random.randint(1,20000))


    for _ in range(100):

        node = random.randint(1,20000)

        start=time.time()

        run_query(depth,node)

        end=time.time()

        times.append(
            (end-start)*1000
        )


    return (
        statistics.median(times),
        sorted(times)[94]
    )


print("\nTraversal Benchmark - Neo4j AuraDB\n")


for depth in [1,2,3]:

    p50,p95=benchmark(depth)

    print(f"{depth}-hop")
    print(f"p50 : {p50:.2f} ms")
    print(f"p95 : {p95:.2f} ms")
    print()


driver.close()