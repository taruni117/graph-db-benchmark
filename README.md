\# Graph Database Cloud Benchmarking: CognoDB vs Neo4j AuraDB



\## Overview



This project benchmarks \*\*CognoDB Cloud\*\* against \*\*Neo4j AuraDB\*\* using a reproducible graph database workload.



The goal is to compare:



\- Query throughput (QPS)

\- Average query latency

\- P95 latency

\- Mixed read/write performance



The benchmark uses the same workload pattern for both databases to provide a fair comparison.



\---



\# Databases Tested



\## CognoDB Cloud



A managed graph database platform evaluated using:



\- Lookup workload

\- Aggregation workload

\- Mixed workload





\## Neo4j AuraDB



Managed Neo4j cloud database tested using:



\- Mixed read/write workload

\- Bolt protocol connection



\---



\# Benchmark Environment



| Component | Details |

|---|---|

| Operating System | Windows |

| Language | Python 3 |

| Concurrency | 10 clients |

| Total Queries | 1000 |

| Workload | 80% Read / 20% Write |

| Driver | Neo4j Python Driver |

| Test Type | Cloud Database Benchmark |



\---



\# Workload Design



\## Mixed Workload



The workload simulates a typical graph application:



\- 80% read operations

\- 20% write operations

\- 1000 total queries

\- 10 concurrent workers





Operations include:



\### Read



Lookup existing graph entities.



\### Write



Update graph entity properties.



\---



\# Benchmark Methodology



For each database:



1\. Establish database connection.

2\. Execute 1000 mixed queries.

3\. Run with 10 concurrent clients.

4\. Measure:

&#x20;  - Total execution time

&#x20;  - Queries per second

&#x20;  - Average latency

&#x20;  - P95 latency

5\. Store results as JSON.

6\. Generate comparison CSV and charts.



\---



\# Results



\## Mixed Workload Performance



| Database | Queries | Time | QPS | Avg Latency | P95 Latency |

|---|---:|---:|---:|---:|---:|

| Neo4j AuraDB | 1000 | 16.37 sec | 61.09 | 163.13 ms | 275.66 ms |

| CognoDB | 1000 | 1.07 sec | 937.32 | 10.50 ms | 10.84 ms |



\---



\# Performance Comparison



\## Throughput



CognoDB achieved higher throughput in this benchmark:



\- CognoDB: 937.32 QPS

\- Neo4j AuraDB: 61.09 QPS



\## Latency



Average latency:



\- CognoDB: 10.50 ms

\- Neo4j AuraDB: 163.13 ms





P95 latency:



\- CognoDB: 10.84 ms

\- Neo4j AuraDB: 275.66 ms



\---



\# Benchmark Charts



\## QPS Comparison



!\[QPS Comparison](charts/qps\_comparison.png)





\## Average Latency Comparison



!\[Latency Comparison](charts/latency\_comparison.png)





\## P95 Latency Comparison



!\[P95 Latency Comparison](charts/p95\_latency\_comparison.png)



\---



\# Project Structure



