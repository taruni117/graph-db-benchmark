from neo4j import GraphDatabase
from config import COGNODB_URI, COGNODB_USER, COGNODB_PASSWORD

driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USER, COGNODB_PASSWORD)
)

try:
    with driver.session() as session:
        result = session.run("RETURN 'Connection Successful!' AS message")
        print(result.single()["message"])
finally:
    driver.close()