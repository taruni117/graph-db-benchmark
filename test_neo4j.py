from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

try:
    driver.verify_connectivity()
    print("✅ Neo4j AuraDB Connected Successfully!")

    with driver.session() as session:
        result = session.run("RETURN 'Hello Neo4j AuraDB' AS message")
        print(result.single()["message"])

except Exception as e:
    print("❌ Connection failed:")
    print(e)

finally:
    driver.close()