#!/usr/bin/env python3
"""
LifeTree Core Engine Performance Benchmarking Suite
Benchmarking Monte Carlo stochastic simulations (10k & 100k trials) and SQLite FTS5 bulk insert/search.
Supports CLI --quick argument flag and uses isolated temporary databases.
"""

import os
import sys
import time
import json
import sqlite3
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "simulation_engines"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "graph_engines"))

import monte_carlo_decision_engine
from sqlite_graph_store import LifeTreeSQLiteStore

def benchmark_monte_carlo_10k_trials(is_quick: bool = False) -> dict:
    trials = 1000 if is_quick else 10000
    cfg = {"name": "Benchmark Pathway", "base_time_months": 24, "base_cost_usd": 15000.0, "baseline_success_prob": 0.85, "random_seed": 42}

    t0 = time.perf_counter()
    res = monte_carlo_decision_engine.run_monte_carlo_simulation(cfg, num_trials=trials)
    t1 = time.perf_counter()

    duration = round(t1 - t0, 4)
    ops_per_sec = round(trials / duration, 2) if duration > 0 else 0.0

    output = {"benchmark": "benchmark_monte_carlo_10k_trials", "trials": trials, "duration_seconds": duration, "ops_per_second": ops_per_sec}
    print(json.dumps(output, ensure_ascii=False))

    if not is_quick:
        assert duration < 2.0, f"Monte Carlo 10k trials exceeded 2.0s threshold! ({duration}s)"

    return output

def benchmark_monte_carlo_100k_trials(is_quick: bool = False) -> dict:
    trials = 5000 if is_quick else 100000
    cfg = {"name": "Benchmark Pathway 100k", "base_time_months": 24, "base_cost_usd": 15000.0, "baseline_success_prob": 0.85, "random_seed": 42}

    t0 = time.perf_counter()
    res = monte_carlo_decision_engine.run_monte_carlo_simulation(cfg, num_trials=trials)
    t1 = time.perf_counter()

    duration = round(t1 - t0, 4)
    ops_per_sec = round(trials / duration, 2) if duration > 0 else 0.0

    output = {"benchmark": "benchmark_monte_carlo_100k_trials", "trials": trials, "duration_seconds": duration, "ops_per_second": ops_per_sec}
    print(json.dumps(output, ensure_ascii=False))

    return output

def benchmark_sqlite_fts_insert_1000_nodes(is_quick: bool = False) -> dict:
    nodes_count = 100 if is_quick else 1000
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "benchmark_fts.db")
        store = LifeTreeSQLiteStore(db_path)

        t0 = time.perf_counter()
        for i in range(nodes_count):
            nid = f"node_bench_{i:04d}"
            label = f"Statutory Regulation Section {i} on Immigration & Taxes"
            store.upsert_node({
                "id": nid,
                "label": label,
                "entity_type": "REGULATION_LAW",
                "confidence": 0.95
            })
        t1 = time.perf_counter()
        store.close()

        duration = round(t1 - t0, 4)
        ops_per_sec = round(nodes_count / duration, 2) if duration > 0 else 0.0

        output = {"benchmark": "benchmark_sqlite_fts_insert_1000_nodes", "trials": nodes_count, "duration_seconds": duration, "ops_per_second": ops_per_sec}
        print(json.dumps(output, ensure_ascii=False))

        if not is_quick:
            assert duration < 5.0, f"SQLite FTS insert 1000 nodes exceeded 5.0s threshold! ({duration}s)"

        return output

def benchmark_sqlite_fts_search_100_queries(is_quick: bool = False) -> dict:
    queries_count = 20 if is_quick else 100
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "benchmark_search.db")
        store = LifeTreeSQLiteStore(db_path)

        # Seed database with 500 nodes
        for i in range(500):
            nid = f"node_search_{i:04d}"
            label = f"Immigration Sperrkonto Regulation Section {i}"
            store.upsert_node({
                "id": nid,
                "label": label,
                "entity_type": "REGULATION_LAW",
                "confidence": 0.95
            })

        t0 = time.perf_counter()
        for _ in range(queries_count):
            store.fts_search_nodes("Immigration Sperrkonto")
        t1 = time.perf_counter()
        store.close()

        duration = round(t1 - t0, 4)
        avg_latency = round(duration / queries_count, 4)
        ops_per_sec = round(queries_count / duration, 2) if duration > 0 else 0.0

        output = {"benchmark": "benchmark_sqlite_fts_search_100_queries", "trials": queries_count, "duration_seconds": duration, "ops_per_second": ops_per_sec}
        print(json.dumps(output, ensure_ascii=False))

        if not is_quick:
            assert avg_latency < 0.10, f"SQLite FTS search average latency exceeded 0.10s threshold! ({avg_latency}s)"

        return output

def main():
    is_quick = "--quick" in sys.argv
    print("=" * 80)
    print(f"⚡ RUNNING LIFETREE BENCHMARKING SUITE ({'QUICK MODE' if is_quick else 'FULL MODE'})")
    print("=" * 80)

    benchmark_monte_carlo_10k_trials(is_quick)
    benchmark_monte_carlo_100k_trials(is_quick)
    benchmark_sqlite_fts_insert_1000_nodes(is_quick)
    benchmark_sqlite_fts_search_100_queries(is_quick)

    print("=" * 80)
    print("✅ BENCHMARKING COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    main()
