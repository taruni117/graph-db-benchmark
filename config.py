import os
from dotenv import load_dotenv

load_dotenv()

# CognoDB
COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USER = os.getenv("COGNODB_USER")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")

# Neo4j AuraDB
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")