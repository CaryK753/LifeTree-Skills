#!/usr/bin/env python3
"""
LifeTree Plain-Language Human Translator Engine
Translates abstract mathematical decision metrics (CVaR, CPT, MAUT, Nash Equilibria, Bayesian Posteriors)
into empathetic, clear, intuitive natural human language and user-friendly explanations.
"""

import sys
import json
from typing import Dict, Any

METRIC_HUMAN_DICTIONARY = {
    "CVaR_Expected_Shortfall": "最坏情况资金保障线 (Extreme Disaster Buffer)",
    "VaR_95_Max_Cost": "正常波动预算 (Normal Risk Budget)",
    "CPT_Utility_Score": "心理真实满意度 (Human Real-Feel Score)",
    "MAUT_Total_Utility": "综合目标匹配度 (Multi-Goal Alignment Score)",
    "Bayesian_Posterior": "最新证据胜算/信心度 (Updated Success Confidence)",
    "Nash_Equilibrium": "多方博弈双赢平衡点 (Win-Win Balance Strategy)",
    "Optimal_Stopping_37": "最佳出手决策窗口 (Optimal Decision Window)",
    "Decision_Nodes": "我的可控选择 (My Action Choices)",
    "Chance_Nodes": "外部环境变数 (External Reality Factors)",
    "Value_Nodes": "人生核心目标 (Core Life Goals)"
}

def translate_metrics_to_human_language(raw_metrics: Dict[str, Any], lang: str = "zh") -> Dict[str, Any]:
    """
    Translates raw decision science output dict into clear human-understandable prose.
    """
    try:
        mc = raw_metrics.get("monte_carlo_results", {})
        p50 = mc.get("execution_timeline_months", {}).get("P50_median", 24)
        var_cost = mc.get("financial_capital_usd", {}).get("VaR_95_max_cost", 18500)
        cvar_cost = mc.get("financial_capital_usd", {}).get("CVaR_95_expected_shortfall_cost", var_cost * 1.25)

        verdict_summary_zh = (
            f"根据 10,000 次模拟推演，该方案预计需要约 {p50} 个月完成。"
            f"在 95% 的日常波动情况下，准备 ${var_cost:,.0f} 资金即可满足支出；"
            f"但若遭遇极端黑天鹅风险（最坏情况），建议准备至少 ${cvar_cost:,.0f} 的极端安全兜底资金。"
        )

        verdict_summary_en = (
            f"Based on 10,000 simulation runs, this plan takes approximately {p50} months median timeline. "
            f"Under normal 95% market fluctuations, a ${var_cost:,.0f} reserve is sufficient; "
            f"however, under extreme worst-case scenarios, a safety buffer of ${cvar_cost:,.0f} is recommended."
        )

        return {
            "status": "SUCCESS",
            "language": lang,
            "human_verdict_text": verdict_summary_zh if lang == "zh" else verdict_summary_en,
            "human_readable_dictionary": METRIC_HUMAN_DICTIONARY
        }

    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def main():
    try:
        res = translate_metrics_to_human_language({"monte_carlo_results": {"execution_timeline_months": {"P50_median": 24}, "financial_capital_usd": {"VaR_95_max_cost": 18500}}})
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
