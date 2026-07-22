#!/usr/bin/env python3
"""
LifeTree Unit Tests for Simulation & Decision Engines
Tests Monte Carlo 10k simulations, Tornado Diagrams, Sensitivity Elasticity, and Stakeholder Solver.
"""

import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "simulation_engines"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts", "decision_analysis"))

import monte_carlo_decision_engine
import tornado_diagram_engine
import graph_sensitivity_engine
import game_theory_stakeholder_solver
import confidence_decay_pattern_engine

class TestSimulationEngines(unittest.TestCase):

    def test_monte_carlo_10k_trials(self):
        cfg = {"name": "Test Pathway", "base_time_months": 24, "base_cost_usd": 15000.0, "baseline_success_prob": 0.85}
        res = monte_carlo_decision_engine.run_monte_carlo_simulation(cfg, num_trials=1000)
        self.assertIn("monte_carlo_results", res)
        mc = res["monte_carlo_results"]
        self.assertEqual(mc["total_trials_simulated"], 1000)
        self.assertIn("VaR_95_max_timeline", mc["execution_timeline_months"])

    def test_tornado_diagram_derivative_calculation(self):
        res = tornado_diagram_engine.calculate_tornado_sensitivity_swings({"base_success_prob": 0.85})
        self.assertEqual(res["status"], "SUCCESS")
        swings = res["tornado_diagram_swings"]
        self.assertTrue(len(swings) > 0)
        self.assertTrue(swings[0]["volatility_swing"] >= swings[-1]["volatility_swing"])

    def test_graph_sensitivity_roi_elasticity(self):
        prof = {"german_level": "A2", "liquid_funds_usd": 35000.0, "work_experience_years": 4}
        res = graph_sensitivity_engine.calculate_parameter_sensitivity(prof)
        self.assertEqual(res["status"], "SUCCESS")
        rois = res["ranked_personal_action_rois"]
        self.assertTrue(len(rois) > 0)

    def test_game_theory_stakeholder_solver(self):
        reqs = [
            {"stakeholder": "Host Immigration Board", "category": "IMMIGRATION_PHYSICAL_PRESENCE"},
            {"stakeholder": "Origin Tax Authority", "category": "TAX_WORLDWIDE_LIABILITY"}
        ]
        res = game_theory_stakeholder_solver.solve_stakeholder_conflicts(reqs)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(len(res["conflicts"]) > 0)

    def test_confidence_decay_exponential(self):
        res = confidence_decay_pattern_engine.calculate_confidence_decay(0.95, 180, 0.002)
        self.assertEqual(res["status"], "SUCCESS")
        calc = res["decay_calculation"]
        self.assertTrue(calc["decayed_confidence"] < 0.95)

if __name__ == "__main__":
    unittest.main()
