#!/usr/bin/env python3
"""
LifeTree Unit Tests for Decision Science & Behavioral Utility Engines
Tests Prospect Theory, MAUT, Influence Diagrams, CVaR Copula, Bayesian Belief, and Optimal Stopping.
"""

import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "decision_analysis"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "graph_engines"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "simulation_engines"))

import utility_theory_engine
import influence_diagram_engine
import tail_risk_cvar_engine
import bayesian_belief_engine
import optimal_stopping_engine

class TestDecisionScienceEngines(unittest.TestCase):

    def test_prospect_theory_loss_aversion(self):
        # Test that losses are weighted heavier due to loss aversion lambda = 2.25
        res_gain = utility_theory_engine.value_function_prospect_theory(100.0)
        res_loss = utility_theory_engine.value_function_prospect_theory(-100.0)
        self.assertTrue(abs(res_loss) > res_gain)

    def test_maut_utility_calculation(self):
        attrs = {"income": 80.0, "health": 85.0, "time_freedom": 60.0, "family_security": 90.0, "stress_inverted": 70.0}
        res = utility_theory_engine.calculate_maut_utility(attrs)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(res["maut_total_utility_score"] > 0)

    def test_influence_diagram_backward_induction(self):
        res = influence_diagram_engine.evaluate_influence_diagram({})
        self.assertEqual(res["status"], "SUCCESS")
        summary = res["influence_diagram_summary"]
        self.assertIn("optimal_decision_policy", summary)

    def test_tail_risk_cvar_and_copula(self):
        res = tail_risk_cvar_engine.simulate_copula_systemic_risks(base_cost=15000.0, correlation_rho=0.65, num_trials=1000)
        self.assertEqual(res["status"], "SUCCESS")
        copula = res["copula_simulation"]
        self.assertTrue(copula["cvar_expected_shortfall_usd"] >= copula["var_95_max_cost_usd"])

    def test_bayesian_belief_updating(self):
        res = bayesian_belief_engine.update_bayesian_belief(0.85, 0.90, 0.20)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(res["posterior_probability_P_H_given_E"] > 0.85)

    def test_optimal_stopping_and_hyperbolic_discounting(self):
        os_res = optimal_stopping_engine.calculate_optimal_stopping_threshold(10)
        hd_res = optimal_stopping_engine.calculate_hyperbolic_discounting(100000.0, 5.0)
        self.assertEqual(os_res["status"], "SUCCESS")
        self.assertEqual(hd_res["status"], "SUCCESS")
        self.assertTrue(hd_res["hyperbolic_present_utility_usd"] < 100000.0)

if __name__ == "__main__":
    unittest.main()
