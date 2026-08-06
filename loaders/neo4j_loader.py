import csv
import time
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

NODE_FILE = "datasets/nodes.csv"
EDGE_FILE = "datasets/edges.csv"


def clear_database():
    print("Clearing database...")
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    print("Database cleared.")


def create_index():
    print("Creating index...")
    with driver.session() as session:
        session.run(
            "CREATE INDEX person_id IF NOT EXISTS FOR (p:Person) ON (p.id)"
        )
    print("Index created.")


def load_nodes():
    print("Loading nodes...")
    start = time.time()

    with driver.session() as session:
        with open(NODE_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            batch = []

            for row in reader:
                batch.append(
                    {
                        "id": int(row["id"]),
                        "name": row["name"]
                    }
                )

                if len(batch) == 1000:
                    session.run(
                        """
                        UNWIND $rows AS row
                        CREATE (:Person {
                            id: row.id,
                            name: row.name
                        })
                        """,
                        rows=batch,
                    )
                    batch = []

            if batch:
                session.run(
                    """
                    UNWIND $rows AS row
                    CREATE (:Person {
                        id: row.id,
                        name: row.name
                    })
                    """,
                    rows=batch,
                )

    elapsed = time.time() - start
    print(f"Nodes loaded in {elapsed:.2f} sec")
    return elapsed


def load_relationships():
    print("Loading relationships...")
    start = time.time()

    with driver.session() as session:
        with open(EDGE_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            batch = []

            for row in reader:
                batch.append(
                    {
                        "source": int(row["source"]),
                        "target": int(row["target"]),
                    }
                )

                if len(batch) == 1000:
                    session.run(
                        """
                        UNWIND $rows AS row
                        MATCH (a:Person {id: row.source})
                        MATCH (b:Person {id: row.target})
                        CREATE (a)-[:FRIEND]->(b)
                        """,
                        rows=batch,
                    )
                    batch = []

            if batch:
                session.run(
                    """
                    UNWIND $rows AS row
                    MATCH (a:Person {id: row.source})
                    MATCH (b:Person {id: row.target})
                    CREATE (a)-[:FRIEND]->(b)
                    """,
                    rows=batch,
                )

    elapsed = time.time() - start
    print(f"Relationships loaded in {elapsed:.2f} sec")
    return elapsed


def count_data():
    with driver.session() as session:
        nodes = session.run(
            "MATCH (n) RETURN count(n) AS c"
        ).single()["c"]

        rels = session.run(
            "MATCH ()-[r]->() RETURN count(r) AS c"
        ).single()["c"]

    print("\n==============================")
    print("Nodes          :", nodes)
    print("Relationships  :", rels)
    print("==============================")


if __name__ == "__main__":
    clear_database()
    create_index()

    node_time = load_nodes()
    rel_time = load_relationships()

    count_data()

    print("\n========= Benchmark =========")
    print(f"Node Load Time : {node_time:.2f} sec")
    print(f"Rel Load Time  : {rel_time:.2f} sec")
    print(f"Total Load     : {node_time + rel_time:.2f} sec")
    print("=============================")

    driver.close()