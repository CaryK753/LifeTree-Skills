#!/usr/bin/env python3
"""
LifeTree Unit Tests for Decision Science & Behavioral Utility Engines
Tests Prospect Theory, MAUT, Influence Diagrams, CVaR Copula, Bayesian Belief, and Optimal Stopping.

Bug 3: Updated imports — utility_theory_engine & bayesian_belief_engine (decision_analysis/)
deleted; tests now use the canonical decision_models/ versions.
"""

import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "decision_models"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "graph_engines"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "simulation_engines"))

# Bug 3: use canonical decision_models/ engines
import prospect_theory_engine       # was utility_theory_engine
import maut_utility_engine          # was utility_theory_engine.calculate_maut_utility
import bayesian_belief_updater      # was bayesian_belief_engine
import influence_diagram_engine
import tail_risk_cvar_engine
import optimal_stopping_engine

class TestDecisionScienceEngines(unittest.TestCase):

    def test_prospect_theory_loss_aversion(self):
        # Test that losses are weighted heavier due to loss aversion lambda = 2.25
        res_gain = prospect_theory_engine.value_function_prospect_theory(100.0)
        res_loss = prospect_theory_engine.value_function_prospect_theory(-100.0)
        self.assertTrue(abs(res_loss) > res_gain)

    def test_maut_utility_calculation(self):
        attrs = {"income": 80.0, "health": 85.0, "time_cost_inverted": 70.0, "family_stability": 90.0, "stress_inverted": 70.0}
        res = maut_utility_engine.evaluate_maut_utility(attrs)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(res["maut_total_utility_score"] > 0)

    def test_influence_diagram_backward_induction(self):
        # C5 fix: empty payload must NOT silently substitute hardcoded defaults.
        # It should return an explicit NO_DECISION_NODES error so callers know no
        # real decision modeling happened.
        empty_res = influence_diagram_engine.evaluate_influence_diagram({})
        self.assertEqual(empty_res["status"], "ERROR")
        self.assertEqual(empty_res["error_code"], "NO_DECISION_NODES")

        # Opt-in defaults carry used_default_payload=true so downstream UIs can warn.
        opt_in_res = influence_diagram_engine.evaluate_influence_diagram({"use_defaults_if_empty": True})
        self.assertEqual(opt_in_res["status"], "SUCCESS")
        self.assertTrue(opt_in_res["used_default_payload"])

        # Real payload performs actual backward induction.
        res = influence_diagram_engine.evaluate_influence_diagram({
            "decision_nodes": [{"id": "d_visa_route", "label": "Visa Path Choice",
                                "options": ["CHANCENKARTE_ROUTE", "DIRECT_EMPLOYER_ROUTE"]}],
            "chance_nodes": [
                {"id": "c_chancen", "parent_option": "CHANCENKARTE_ROUTE",
                 "outcomes": [{"state": "SUCCESS", "prob": 0.88}, {"state": "DELAY", "prob": 0.12}]},
                {"id": "c_direct", "parent_option": "DIRECT_EMPLOYER_ROUTE",
                 "outcomes": [{"state": "SUCCESS", "prob": 0.70}, {"state": "REJECT", "prob": 0.30}]}
            ],
            "value_nodes": [
                {"parent_option": "CHANCENKARTE_ROUTE", "state": "SUCCESS", "utility_value": 90.0},
                {"parent_option": "CHANCENKARTE_ROUTE", "state": "DELAY", "utility_value": 30.0},
                {"parent_option": "DIRECT_EMPLOYER_ROUTE", "state": "SUCCESS", "utility_value": 95.0},
                {"parent_option": "DIRECT_EMPLOYER_ROUTE", "state": "REJECT", "utility_value": -50.0}
            ]
        })
        self.assertEqual(res["status"], "SUCCESS")
        self.assertFalse(res["used_default_payload"])
        summary = res["influence_diagram_summary"]
        self.assertIn("optimal_decision_policy", summary)

    def test_tail_risk_cvar_and_copula(self):
        res = tail_risk_cvar_engine.simulate_copula_systemic_risks(base_cost=15000.0, correlation_rho=0.65, num_trials=1000)
        self.assertEqual(res["status"], "SUCCESS")
        copula = res["copula_simulation"]
        self.assertTrue(copula["cvar_expected_shortfall_usd"] >= copula["var_95_max_cost_usd"])

    def test_bayesian_belief_updating(self):
        # Bug 3: now uses bayesian_belief_updater (was bayesian_belief_engine)
        res = bayesian_belief_updater.update_bayesian_belief(0.85, 0.90, 0.20)
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
