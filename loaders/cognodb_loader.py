import os
import sys
import csv
import time
from neo4j import GraphDatabase

# Allow importing config.py from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import (
    COGNODB_URI,
    COGNODB_USER,
    COGNODB_PASSWORD
)

BATCH_SIZE = 1000

driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USER, COGNODB_PASSWORD)
)


def run_query(query, **params):
    with driver.session() as session:
        session.run(query, **params)


def clear_database():
    print("Clearing database...")
    run_query("MATCH (n) DETACH DELETE n")
    print("Database cleared.\n")


def create_index():
    print("Creating index...")

    run_query("""
    CREATE INDEX person_id_index IF NOT EXISTS
    FOR (p:Person)
    ON (p.id)
    """)

    print("Index created.\n")


def load_nodes():

    print("Loading nodes...")

    start = time.perf_counter()

    with driver.session() as session:

        batch = []

        with open("datasets/nodes.csv", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                batch.append({
                    "id": int(row["id"]),
                    "name": row["name"]
                })

                if len(batch) >= BATCH_SIZE:

                    session.run("""
                    UNWIND $rows AS row
                    CREATE (:Person {
                        id: row.id,
                        name: row.name
                    })
                    """, rows=batch)

                    batch = []

            if batch:

                session.run("""
                UNWIND $rows AS row
                CREATE (:Person {
                    id: row.id,
                    name: row.name
                })
                """, rows=batch)

    elapsed = time.perf_counter() - start

    print(f"Nodes loaded in {elapsed:.2f} seconds.\n")

    return elapsed


def load_edges():

    print("Loading relationships...")

    start = time.perf_counter()

    with driver.session() as session:

        batch = []

        with open("datasets/edges.csv", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                batch.append({
                    "source": int(row["source"]),
                    "target": int(row["target"])
                })

                if len(batch) >= BATCH_SIZE:

                    session.run("""
                    UNWIND $rows AS row
                    MATCH (a:Person {id: row.source})
                    MATCH (b:Person {id: row.target})
                    CREATE (a)-[:KNOWS]->(b)
                    """, rows=batch)

                    batch = []

            if batch:

                session.run("""
                UNWIND $rows AS row
                MATCH (a:Person {id: row.source})
                MATCH (b:Person {id: row.target})
                CREATE (a)-[:KNOWS]->(b)
                """, rows=batch)

    elapsed = time.perf_counter() - start

    print(f"Relationships loaded in {elapsed:.2f} seconds.\n")

    return elapsed


def print_counts():

    with driver.session() as session:

        nodes = session.run(
            "MATCH (n:Person) RETURN count(n) AS total"
        ).single()["total"]

        edges = session.run(
            "MATCH ()-[r:KNOWS]->() RETURN count(r) AS total"
        ).single()["total"]

    print("===================================")
    print(f"Total Nodes         : {nodes}")
    print(f"Total Relationships : {edges}")
    print("===================================\n")


def main():

    overall = time.perf_counter()

    clear_database()

    create_index()

    node_time = load_nodes()

    edge_time = load_edges()

    total = time.perf_counter() - overall

    print_counts()

    print("========== Benchmark ==========")
    print(f"Node Load Time        : {node_time:.2f} sec")
    print(f"Relationship Load Time: {edge_time:.2f} sec")
    print(f"Total Load Time       : {total:.2f} sec")
    print("===============================")

    driver.close()


if __name__ == "__main__":
    main()