#!/usr/bin/env python3
"""
LifeTree Unit Tests for Graph Engines
Tests Dijkstra pathfinding, SQLite storage, FTS5 search, and Graph Visualizers.
"""

import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "graph_engines"))

import temporal_graph_engine
import sqlite_graph_store
import graph_visualizer_html

class TestGraphEngines(unittest.TestCase):

    def setUp(self):
        self.sample_ontology = {
            "nodes": [
                {"id": "usr_person", "label": "Person (Applicant)", "entity_type": "PERSON", "confidence": 1.0},
                {"id": "asset_sperrkonto", "label": "€12,000 Blocked Account", "entity_type": "CAPITAL_ASSET", "confidence": 1.0},
                {"id": "route_bluecard", "label": "EU Blue Card Permit", "entity_type": "PATHWAY_ROUTE", "confidence": 1.0}
            ],
            "edges": [
                {"source": "usr_person", "target": "asset_sperrkonto", "relation_type": "REQUIRES_CAPITAL", "confidence": 1.0, "kinetic_weight": 1.0},
                {"source": "asset_sperrkonto", "target": "route_bluecard", "relation_type": "CONVERTS_TO", "confidence": 1.0, "kinetic_weight": 1.0}
            ]
        }

    def test_dijkstra_optimal_path(self):
        res = temporal_graph_engine.find_optimal_causal_path(self.sample_ontology, "usr_person", "route_bluecard")
        self.assertIn("pathfinding_summary", res)
        self.assertIn("path_nodes", res)
        self.assertEqual(len(res["path_nodes"]), 3)

    def test_sqlite_db_init_and_fts_search(self):
        db_path = os.path.join(SKILL_ROOT, "resources", "database", "test_lifetree.sqlite")
        store = sqlite_graph_store.LifeTreeSQLiteStore(db_path)
        store.upsert_node({"id": "n_test_1", "label": "Test Person Node", "entity_type": "PERSON", "properties": {"age": 30}})

        search_res = store.fts_search_nodes("Test")
        self.assertTrue(len(search_res) > 0)
        self.assertEqual(search_res[0]["id"], "n_test_1")
        store.close()

        if os.path.exists(db_path):
            os.remove(db_path)

    def test_graph_visualizer_html_generation(self):
        out_html = os.path.join(SKILL_ROOT, "examples", "test_graph_viewer.html")
        res_path = graph_visualizer_html.generate_graph_visualizer_html(self.sample_ontology, out_html)
        self.assertTrue(os.path.exists(res_path))
        if os.path.exists(res_path):
            os.remove(res_path)

if __name__ == "__main__":
    unittest.main()
