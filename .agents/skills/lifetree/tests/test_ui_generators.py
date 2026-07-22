#!/usr/bin/env python3
"""
LifeTree Unit Tests for UI & HTML Dashboard Generators
Verifies that HTML Decision Dashboards, Graph Viewers, Deduction Players, and Growing Trees render cleanly.
"""

import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "ui_translators"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "graph_engines"))

import html_report_generator
import graph_visualizer_html
import deduction_player_html
import growing_tree_html

class TestUIGenerators(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            "monte_carlo_results": {
                "execution_timeline_months": {"P50_median": 24.1, "P90_pessimistic": 31.8},
                "financial_capital_usd": {"VaR_95_max_cost": 18508.22}
            },
            "weekly_action_checklist": [
                {"task_title": "Top ROI Action", "action_details": "Upgrade German A2 to B1", "priority": "HIGH", "target_deadline": "Within 7 Days"}
            ],
            "regret_audit": {"audit_summary": {"regret_minimization_index": 93.2}},
            "deduction_summary": {"timeline_horizon_years": 5, "recommended_branch": "Pathway A"},
            "pathway_a_trajectory": [
                {"year": 1, "success_probability": 0.85, "capital_balance_usd": 26000.0, "events": ["Start"], "badge": "OPTIMAL_PROGRESSION"}
            ],
            "pathway_b_trajectory": [
                {"year": 1, "success_probability": 0.70, "capital_balance_usd": 35000.0, "events": ["Start"], "badge": "HIGH_FRICTION_PROGRESSION"}
            ]
        }
        self.sample_ontology = {
            "nodes": [{"id": "usr_person", "label": "Person", "entity_type": "PERSON"}],
            "edges": []
        }

    def test_interactive_html_report_generator(self):
        out_path = os.path.join(SKILL_ROOT, "examples", "test_report.html")
        res_path = html_report_generator.generate_interactive_html_report(self.sample_data, out_path)
        self.assertTrue(os.path.exists(res_path))
        with open(res_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("LifeTree", content)
        if os.path.exists(res_path):
            os.remove(res_path)

    def test_deduction_player_html_generator(self):
        out_path = os.path.join(SKILL_ROOT, "examples", "test_deduction_player.html")
        res_path = deduction_player_html.generate_deduction_player_html(self.sample_data, out_path)
        self.assertTrue(os.path.exists(res_path))
        with open(res_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("Temporal Deduction Player", content)
        if os.path.exists(res_path):
            os.remove(res_path)

    def test_growing_tree_html_generator(self):
        out_path = os.path.join(SKILL_ROOT, "examples", "test_growing_tree.html")
        res_path = growing_tree_html.generate_growing_tree_html(self.sample_data, out_path)
        self.assertTrue(os.path.exists(res_path))
        with open(res_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("Growing Decision Tree", content)
        if os.path.exists(res_path):
            os.remove(res_path)

if __name__ == "__main__":
    unittest.main()
