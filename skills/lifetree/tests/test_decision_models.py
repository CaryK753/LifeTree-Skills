#!/usr/bin/env python3
"""
LifeTree Unit Tests for ./scripts/decision_models/ Modules
Tests MAUT+AHP, CVaR Expected Shortfall, Influence Diagrams, Bayesian Belief, Intertemporal Discounting,
Optimal Stopping, Copula Correlation, Prospect Theory, and Markov Transitions.
"""

import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "decision_models"))

import maut_utility_engine
import cvar_risk_engine
import influence_diagram_layer
import bayesian_belief_updater
import intertemporal_discounting_engine
import optimal_stopping_solver
import copula_correlation_engine
import prospect_theory_engine
import markov_transition_engine

class TestDecisionModelsFolder(unittest.TestCase):

    def test_maut_and_ahp_calculation(self):
        scores = {"income": 80.0, "health": 85.0, "time_cost_inverted": 70.0}
        res = maut_utility_engine.evaluate_maut_utility(scores)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(res["maut_total_utility_score"] > 0)

    def test_cvar_expected_shortfall_metrics(self):
        costs = [10000.0 * (i / 100.0) for i in range(1, 101)]
        res = cvar_risk_engine.calculate_cvar_metrics(costs, alpha=0.95, initial_capital_usd=8000.0)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(res["cvar_expected_shortfall_usd"] >= res["var_95_max_cost_usd"])

    def test_influence_diagram_layer_tagging(self):
        g = {"nodes": [{"id": "n1", "label": "Visa Action", "entity_type": "ACTION"}], "edges": []}
        res = influence_diagram_layer.construct_influence_diagram_layer(g)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["influence_nodes"][0]["influence_node_type"], "DECISION_NODE")

    def test_bayesian_belief_updater_and_dempster_combination(self):
        res_b = bayesian_belief_updater.update_posterior_belief(0.80, 0.90, 0.20)
        m1 = {"TRUE": 0.60, "FALSE": 0.10, "UNCERTAIN": 0.30}
        m2 = {"TRUE": 0.70, "FALSE": 0.05, "UNCERTAIN": 0.25}
        res_ds = bayesian_belief_updater.combine_dempster_shafer_evidence(m1, m2)
        self.assertEqual(res_b["status"], "SUCCESS")
        self.assertEqual(res_ds["status"], "SUCCESS")

    def test_intertemporal_discounting(self):
        res = intertemporal_discounting_engine.calculate_intertemporal_discounting(100000.0, 5.0)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(res["hyperbolic_discounted_utility_usd"] < 100000.0)

    def test_optimal_stopping_solver(self):
        res = optimal_stopping_solver.solve_optimal_stopping(10, 2)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["optimal_stopping"]["observation_cutoff_k"], 3)

    def test_copula_correlation(self):
        res = copula_correlation_engine.simulate_gaussian_copula_shocks(40000.0, 0.65, 1000)
        self.assertEqual(res["status"], "SUCCESS")

    def test_prospect_theory(self):
        a = [{"payoff_usd": 30000.0, "prob": 0.80}]
        b = [{"payoff_usd": 18000.0, "prob": 1.00}]
        res = prospect_theory_engine.evaluate_prospect_theory(a, b)
        self.assertEqual(res["status"], "SUCCESS")

    def test_markov_state_transitions(self):
        res = markov_transition_engine.simulate_markov_transitions({}, {}, steps_n=5)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(len(res["step_by_step_trajectory"]), 6)

if __name__ == "__main__":
    unittest.main()
