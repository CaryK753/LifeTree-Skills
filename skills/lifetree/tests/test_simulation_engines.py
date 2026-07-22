#!/usr/bin/env python3
"""
LifeTree Unit Tests for Simulation & Decision Engines
Tests Monte Carlo 10k simulations, Combinatorial Divergent Risk Generator, 2x2 Nash Equilibrium Solver,
and Dynamic MAUT Profile Mapping.
"""

import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "simulation_engines"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "decision_analysis"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "risk_surveillance"))

import monte_carlo_decision_engine
import tornado_diagram_engine
import graph_sensitivity_engine
import game_theory_stakeholder_solver
import confidence_decay_pattern_engine
import divergent_risk_discovery

class TestSimulationEngines(unittest.TestCase):

    def test_monte_carlo_10k_trials(self):
        cfg = {"name": "Test Pathway", "base_time_months": 24, "base_cost_usd": 15000.0, "baseline_success_prob": 0.85}
        res = monte_carlo_decision_engine.run_monte_carlo_simulation(cfg, num_trials=1000)
        self.assertIn("monte_carlo_results", res)
        mc = res["monte_carlo_results"]
        self.assertEqual(mc["total_trials_simulated"], 1000)
        self.assertIn("VaR_95_max_timeline", mc["execution_timeline_months"])
        self.assertIn("CVaR_95_expected_shortfall_cost", mc["financial_capital_usd"])

    def test_tornado_diagram_derivative_calculation(self):
        res = tornado_diagram_engine.calculate_tornado_sensitivity_swings({"base_success_prob": 0.85})
        self.assertEqual(res["status"], "SUCCESS")
        swings = res["tornado_diagram_swings"]
        self.assertTrue(len(swings) > 0)
        self.assertTrue(swings[0]["volatility_swing"] >= swings[-1]["volatility_swing"])

    def test_graph_sensitivity_roi_elasticity_and_maut_mapping(self):
        prof = {
            "german_level": "A2",
            "liquid_funds_usd": 35000.0,
            "annual_income_usd": 70000.0,
            "work_experience_years": 4,
            "nationality": "CN",
            "dependents": 1
        }
        res = graph_sensitivity_engine.calculate_parameter_sensitivity(prof)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("mapped_maut_base_scores", res)
        base_scores = res["mapped_maut_base_scores"]
        self.assertIn("income", base_scores)
        self.assertIn("time_cost_inverted", base_scores)
        rois = res["ranked_personal_action_rois"]
        self.assertTrue(len(rois) > 0)

    def test_game_theory_nash_equilibrium_scenarios(self):
        # Scenario 1: Pure Strategy NE
        st_a = {"stakeholder": "Player A", "preference_vector": {"compliance_cost": -0.2, "penalty_risk": -0.6, "benefit": 1.2}}
        st_b = {"stakeholder": "Player B", "preference_vector": {"compliance_cost": -0.1, "penalty_risk": -0.8, "benefit": 0.9}}
        res_pure = game_theory_stakeholder_solver.solve_stakeholder_conflicts([st_a, st_b])
        self.assertEqual(res_pure["status"], "SUCCESS")
        self.assertEqual(res_pure["solver_mode"], "2X2_NASH_EQUILIBRIUM_SOLVER")
        self.assertIn("pure_strategy_nash_equilibria", res_pure)

        # Scenario 2: Mixed Strategy NE Matrix
        matrix_mixed = [[(2.0, 0.0), (0.0, 1.0)], [(0.0, 1.0), (1.0, 0.0)]]
        mixed_ne = game_theory_stakeholder_solver.find_mixed_strategy_nash_equilibrium(matrix_mixed)
        self.assertTrue(0.0 <= mixed_ne["prob_a_play_cooperate"] <= 1.0)

        # Scenario 3: Fallback Rule Matching (no preference_vector)
        st_rule_a = {"stakeholder": "Immigration", "category": "IMMIGRATION_PHYSICAL_PRESENCE"}
        st_rule_b = {"stakeholder": "Tax Office", "category": "TAX_WORLDWIDE_LIABILITY"}
        res_fallback = game_theory_stakeholder_solver.solve_stakeholder_conflicts([st_rule_a, st_rule_b])
        self.assertEqual(res_fallback["status"], "SUCCESS")
        self.assertEqual(res_fallback["solver_mode"], "RULE_MATCHING_FALLBACK")
        self.assertTrue(len(res_fallback["conflicts"]) > 0)

    def test_combinatorial_divergent_risk_discovery(self):
        # Topic combination 1: IMMIGRATION + ASSET
        topics1 = [{"topic_id": "t1", "category": "IMMIGRATION"}, {"topic_id": "t2", "category": "ASSET"}]
        res1 = divergent_risk_discovery.discover_latent_risks(topics1)
        self.assertEqual(res1["status"], "SUCCESS")
        risks1 = res1["discovered_risk_domains"]
        self.assertTrue(any(r["category"] == "IMMIGRATION" for r in risks1))
        self.assertTrue(any(r["category"] == "ASSET" for r in risks1))

        # Topic combination 2: TAX + LEGAL
        topics2 = [{"topic_id": "t3", "category": "TAX"}, {"topic_id": "t4", "category": "LEGAL"}]
        res2 = divergent_risk_discovery.discover_latent_risks(topics2)
        self.assertEqual(res2["status"], "SUCCESS")
        risks2 = res2["discovered_risk_domains"]
        self.assertTrue(any(r["category"] == "TAX" for r in risks2))

        # Topic combination 3: HEALTH + FAMILY
        topics3 = [{"topic_id": "t5", "category": "HEALTH"}, {"topic_id": "t6", "category": "FAMILY"}]
        res3 = divergent_risk_discovery.discover_latent_risks(topics3)
        self.assertEqual(res3["status"], "SUCCESS")
        risks3 = res3["discovered_risk_domains"]
        self.assertTrue(any(r["category"] in ["HEALTH", "FAMILY"] for r in risks3))

    def test_confidence_decay_exponential(self):
        res = confidence_decay_pattern_engine.calculate_confidence_decay(0.95, 180, 0.002)
        self.assertEqual(res["status"], "SUCCESS")
        calc = res["decay_calculation"]
        self.assertTrue(calc["decayed_confidence"] < 0.95)

if __name__ == "__main__":
    unittest.main()
