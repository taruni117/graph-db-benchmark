import json
import time
import random
import concurrent.futures
import sys
import os


from neo4j import GraphDatabase


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD



driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)



latencies = []



def read_query():

    start = time.time()

    query = """
    MATCH (p:Person {id:$id})
    RETURN p.name
    """

    with driver.session() as session:

        session.run(
            query,
            id=random.randint(1,20000)
        ).single()


    latencies.append(
        (time.time() - start) * 1000
    )




def write_query():

    start = time.time()

    query = """
    MATCH (p:Person {id:$id})
    SET p.updated=true
    """

    with driver.session() as session:

        session.run(
            query,
            id=random.randint(1,20000)
        )


    latencies.append(
        (time.time() - start) * 1000
    )




def worker():

    if random.random() < 0.8:

        read_query()

    else:

        write_query()




print("\nMixed Workload - Neo4j AuraDB")
print("-----------------------------")
print("Concurrency: 10 clients")
print("Read/Write mix: 80/20")



start = time.time()


requests = 1000



with concurrent.futures.ThreadPoolExecutor(
    max_workers=10
) as executor:

    futures = []

    for _ in range(requests):

        futures.append(
            executor.submit(worker)
        )


    for future in futures:
        future.result()



elapsed = time.time() - start



qps = requests / elapsed



avg_latency = (
    sum(latencies) / len(latencies)
)


p95_latency = sorted(latencies)[
    int(len(latencies) * 0.95)
]



print("\nResults")
print("----------------")
print("Total Queries :", requests)
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

    "database": "Neo4j AuraDB",

    "workload": "Mixed",

    "read_write_ratio": "80/20",

    "concurrency": 10,

    "total_queries": requests,

    "time_seconds": round(elapsed,2),

    "qps": round(qps,2),

    "average_latency_ms": round(avg_latency,2),

    "p95_latency_ms": round(p95_latency,2)

}



with open(
    "results/neo4j_mixed.json",
    "w"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )



print("\nSaved: results/neo4j_mixed.json")



driver.close()