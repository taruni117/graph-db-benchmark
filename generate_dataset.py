import csv
import random
import os

NUM_NODES = 20000
NUM_EDGES = 150000

os.makedirs("datasets", exist_ok=True)

# Generate nodes
with open("datasets/nodes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name"])

    for i in range(NUM_NODES):
        writer.writerow([i, f"Person_{i}"])

# Generate edges
with open("datasets/edges.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target"])

    edge_count = 0
    while edge_count < NUM_EDGES:
        source = random.randint(0, NUM_NODES - 1)
        target = random.randint(0, NUM_NODES - 1)

        if source != target:
            writer.writerow([source, target])
            edge_count += 1

print("Dataset generated successfully!")
print(f"Nodes: {NUM_NODES}")
print(f"Relationships: {NUM_EDGES}")