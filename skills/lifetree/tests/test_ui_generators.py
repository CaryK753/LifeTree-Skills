#!/usr/bin/env python3
"""
LifeTree Unit Tests for UI Translators & HTML Generators
Tests HTML Dashboard Generator (including Decision Science Cards & Graceful Degradation),
Graph Visualizer HTML, Deduction Player HTML, and Growing Tree HTML.
"""

import os
import sys
import unittest
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "ui_translators"))

import html_report_generator
import graph_visualizer_html
import deduction_player_html
import growing_tree_html

class TestUIGenerators(unittest.TestCase):

    def test_interactive_html_report_generator_full_and_graceful(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            full_out = os.path.join(tmp_dir, "report_full.html")
            data_full = {
                "monte_carlo_results": {
                    "execution_timeline_months": {"P50_median": 24.1, "P90_pessimistic": 31.8},
                    "financial_capital_usd": {"VaR_95_max_cost": 18508.22}
                },
                "weekly_action_checklist": [],
                "tail_risk_results": {"cvar_expected_shortfall_usd": 49103.17, "tail_severity_ratio": 1.289},
                "prospect_theory_results": {"cpt_utility_score": 5423.8, "loss_aversion_lambda": 2.25, "probability_gamma": 0.61},
                "bayesian_belief_results": {"posterior_probability_P_H_given_E": 0.972, "belief_shift_delta": 0.122, "evidence_conflict_k": 0.05},
                "influence_diagram_summary": {"decision_nodes_count": 1, "chance_nodes_count": 3, "value_nodes_count": 1, "causal_intervention_edges_count": 2, "optimal_decision_policy": "CHANCENKARTE_ROUTE"}
            }
            res_path = html_report_generator.generate_interactive_html_report(data_full, full_out)
            self.assertTrue(os.path.exists(res_path))
            with open(res_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("CVaR Tail Risk", content)
                self.assertIn("Prospect Theory", content)
                self.assertIn("Bayesian Belief", content)
                self.assertIn("Influence Diagram Topology Summary", content)

            # Test Graceful Degradation (Missing Decision Science fields)
            minimal_out = os.path.join(tmp_dir, "report_minimal.html")
            data_minimal = {
                "monte_carlo_results": {
                    "execution_timeline_months": {"P50_median": 24.0},
                    "financial_capital_usd": {"VaR_95_max_cost": 15000.0}
                }
            }
            min_path = html_report_generator.generate_interactive_html_report(data_minimal, minimal_out)
            self.assertTrue(os.path.exists(min_path))

    def test_graph_visualizer_html_generation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out = os.path.join(tmp_dir, "graph.html")
            g = {"nodes": [{"id": "n1", "label": "Node 1"}], "edges": []}
            path = graph_visualizer_html.generate_graph_visualizer_html(g, out)
            self.assertTrue(os.path.exists(path))

    def test_deduction_player_html_generator(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out = os.path.join(tmp_dir, "deduction.html")
            ded = {"timeline_projection": [{"year": 2026, "net_worth_usd": 40000}]}
            path = deduction_player_html.generate_deduction_player_html(ded, out)
            self.assertTrue(os.path.exists(path))

    def test_growing_tree_html_generator(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out = os.path.join(tmp_dir, "tree.html")
            ded = {"timeline_projection": [{"year": 2026, "net_worth_usd": 40000}]}
            path = growing_tree_html.generate_growing_tree_html(ded, out)
            self.assertTrue(os.path.exists(path))

if __name__ == "__main__":
    unittest.main()
