#!/usr/bin/env python3
"""
LifeTree Engine Performance & Throughput Benchmark Suite
Measures 10,000-trial Monte Carlo execution time, Dijkstra graph pathfinding latency, and SQLite FTS5 query throughput.
"""

import os
import sys
import time
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "simulation_engines"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "graph_engines"))

import monte_carlo_decision_engine
import temporal_graph_engine
import sqlite_graph_store

def run_performance_benchmarks():
    print("=" * 80)
    print("⚡ RUNNING LIFETREE SYSTEM PERFORMANCE & BENCHMARK SUITE")
    print("=" * 80)

    # 1. Monte Carlo 10,000 Trials Benchmark
    start_mc = time.perf_counter()
    mc_res = monte_carlo_decision_engine.run_monte_carlo_simulation({
        "name": "Benchmark Pathway",
        "base_time_months": 24,
        "base_cost_usd": 15000.0,
        "baseline_success_prob": 0.85,
        "volatility_factor": 0.25
    }, num_trials=10000)
    mc_duration = (time.perf_counter() - start_mc) * 1000.0 # ms
    mc_throughput = 10000.0 / (mc_duration / 1000.0)

    print(f"\n[Benchmark 1] Monte Carlo 10,000 Trials Simulation")
    print(f"  ✓ Execution Time: {mc_duration:.2f} ms")
    print(f"  ✓ Simulation Throughput: {mc_throughput:,.0f} trials/sec")

    # 2. Dijkstra Graph Pathfinding Latency Benchmark
    sample_ontology = {
        "nodes": [{"id": f"node_{i}", "label": f"Node {i}", "entity_type": "CONCEPT"} for i in range(100)],
        "edges": [{"source": f"node_{i}", "target": f"node_{i+1}", "kinetic_weight": 1.0} for i in range(99)]
    }
    start_dijkstra = time.perf_counter()
    path_res = temporal_graph_engine.find_optimal_causal_path(sample_ontology, "node_0", "node_99")
    dijkstra_duration = (time.perf_counter() - start_dijkstra) * 1000.0 # ms

    print(f"\n[Benchmark 2] Dijkstra Causal Pathfinding (100-Node Chain)")
    print(f"  ✓ Execution Time: {dijkstra_duration:.2f} ms")

    # 3. SQLite FTS5 Query Throughput Benchmark
    db_path = os.path.join(SKILL_ROOT, "resources", "database", "benchmark_lifetree.sqlite")
    store = sqlite_graph_store.LifeTreeSQLiteStore(db_path)
    for i in range(500):
        store.upsert_node({"id": f"fts_node_{i}", "label": f"Blocked Account Policy {i}", "entity_type": "REGULATION_LAW"})

    start_fts = time.perf_counter()
    for _ in range(100):
        store.fts_search_nodes("Blocked Account")
    fts_duration = (time.perf_counter() - start_fts) * 1000.0 / 100.0 # avg ms per query

    print(f"\n[Benchmark 3] Embedded SQLite FTS5 Full-Text Search Latency")
    print(f"  ✓ Average Query Latency: {fts_duration:.3f} ms")

    store.close()
    if os.path.exists(db_path):
        os.remove(db_path)

    print("\n" + "=" * 80)
    print("✅ PERFORMANCE BENCHMARK COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_performance_benchmarks()
