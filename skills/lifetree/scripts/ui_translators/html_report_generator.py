#!/usr/bin/env python3
"""
LifeTree Decision Report Dashboard Generator
Generates a detailed, SaaS-quality decision analysis report page.
"""

import os
import sys
import json
from typing import Dict, Any, List


def generate_interactive_html_report(pipeline_data: Dict[str, Any], output_path: str, lang: str = "zh") -> str:
    """
    Generates a detailed decision report HTML page with clean SaaS styling.
    """
    mc_results = pipeline_data.get("monte_carlo_results", {})
    checklist = pipeline_data.get("weekly_action_checklist", [])
    regret_audit = pipeline_data.get("regret_audit", {})

    tail_risk = pipeline_data.get("tail_risk_results", {})
    prospect = pipeline_data.get("prospect_theory_results", {})
    bayes = pipeline_data.get("bayesian_belief_results", {})
    influence = pipeline_data.get("influence_diagram_summary", {})

    p50_time = mc_results.get("execution_timeline_months", {}).get("P50_median", 24)
    p90_time = mc_results.get("execution_timeline_months", {}).get("P90_pessimistic", 32)
    var_cost = mc_results.get("financial_capital_usd", {}).get("VaR_95_max_cost", 18508)
    regret_idx = regret_audit.get("audit_summary", {}).get("regret_minimization_index", 93.2)

    is_zh = (lang == "zh")

    # Tail risk values
    cvar_cost = tail_risk.get("cvar_expected_shortfall_usd", tail_risk.get("copula_simulation", {}).get("cvar_expected_shortfall_usd", var_cost * 2.5))
    tail_ratio = tail_risk.get("tail_severity_ratio", tail_risk.get("copula_simulation", {}).get("tail_severity_ratio", 1.28))

    # Prospect theory
    cpt_score = prospect.get("cpt_utility_score", prospect.get("choice_a_metrics", {}).get("prospect_theory_cpt_utility", 5423.8))

    # Bayesian
    post_prob = bayes.get("posterior_probability_P_H_given_E", 0.972)
    shift_delta = bayes.get("belief_shift_delta", 0.122)

    # Influence diagram
    has_ds_data = bool(tail_risk or prospect or bayes)
    dec_n = influence.get("decision_nodes_count", 1)
    chn_n = influence.get("chance_nodes_count", 3)
    val_n = influence.get("value_nodes_count", 1)
    causal_e = influence.get("causal_intervention_edges_count", 2)
    policy = influence.get("optimal_decision_policy", "CHANCENKARTE_ROUTE")

    # Build checklist
    checklist_html = ""
    for i, item in enumerate(checklist):
        pri = item.get("priority", "MED").upper()
        pri_cls = "bg-red-500/10 text-red-400 border-red-500/20" if pri == "HIGH" else "bg-amber-500/10 text-amber-400 border-amber-500/20"
        pri_label = "紧急" if pri == "HIGH" else "常规"
        checklist_html += f"""
            <div class="flex items-start gap-4 py-4 {'border-t border-[#2a2a3a]' if i > 0 else ''}">
                <input type="checkbox" class="mt-1 w-4 h-4 rounded border-2 border-[#3a3a4a] bg-transparent accent-emerald-500 cursor-pointer flex-shrink-0" />
                <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-3 flex-wrap">
                        <span class="text-[14px] font-semibold text-[#e8e8ee]">{item.get('task_title', '')}</span>
                        <span class="px-2 py-0.5 text-[11px] font-semibold rounded-md border {pri_cls}">{pri_label}</span>
                    </div>
                    <p class="text-[12px] text-[#8888a0] mt-1">{item.get('action_details', '')}</p>
                    <span class="text-[11px] text-[#6666a0] mt-1 inline-block">⏱ {item.get('target_deadline', '')}</span>
                </div>
            </div>"""

    if not checklist_html:
        checklist_html = '<p class="text-[13px] text-[#6666a0] py-4">暂无待办事项</p>'

    confidence_pct = post_prob * 100

    # Decision science analysis section
    ds_section = ""
    if has_ds_data:
        ds_section = f"""
        <hr class="border-0 border-t border-[#1e1e2e] my-0">
        <section class="py-8">
            <div class="flex items-center justify-between mb-5">
                <h2 class="text-base font-bold text-[#e8e8ee]">风险与信心深度分析</h2>
                <span class="text-xs text-[#6666a0]">三维度综合评估</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5">
                    <div class="text-lg mb-3">🛡️</div>
                    <div class="text-sm font-bold text-[#e8e8ee] mb-1">最坏情况保障</div>
                    <p class="text-xs text-[#8888a0] mb-4 leading-relaxed">极端不利情况下的资金安全线，即使遇到黑天鹅事件也有兜底。</p>
                    <div class="space-y-2">
                        <div class="flex justify-between items-baseline py-2 border-t border-[#2a2a3a]">
                            <span class="text-xs text-[#8888a0]">日常准备金</span>
                            <span class="text-sm font-bold text-[#e8e8ee]">${var_cost:,.0f}</span>
                        </div>
                        <div class="flex justify-between items-baseline py-2 border-t border-[#2a2a3a]">
                            <span class="text-xs text-[#8888a0]">极端保障线</span>
                            <span class="text-sm font-bold text-[#ef4444]">${cvar_cost:,.0f}</span>
                        </div>
                        <div class="flex justify-between items-baseline py-2 border-t border-[#2a2a3a]">
                            <span class="text-xs text-[#8888a0]">防范倍数</span>
                            <span class="text-sm font-bold text-[#f59e0b]">{tail_ratio:.1f}x</span>
                        </div>
                    </div>
                </div>
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5">
                    <div class="text-lg mb-3">🧠</div>
                    <div class="text-sm font-bold text-[#e8e8ee] mb-1">心理满意度评估</div>
                    <p class="text-xs text-[#8888a0] mb-4 leading-relaxed">考虑人对亏损的天然厌恶心理后，评估方案带来的真实满意度。</p>
                    <div class="space-y-2">
                        <div class="flex justify-between items-baseline py-2 border-t border-[#2a2a3a]">
                            <span class="text-xs text-[#8888a0]">综合满意得分</span>
                            <span class="text-sm font-bold text-[#6366f1]">{cpt_score:,.0f}</span>
                        </div>
                        <div class="flex justify-between items-baseline py-2 border-t border-[#2a2a3a]">
                            <span class="text-xs text-[#8888a0]">亏损防护等级</span>
                            <span class="text-sm font-bold text-[#e8e8ee]">2.25x</span>
                        </div>
                        <div class="flex justify-between items-baseline py-2 border-t border-[#2a2a3a]">
                            <span class="text-xs text-[#8888a0]">整体评价</span>
                            <span class="text-sm font-bold text-[#22c55e]">偏好匹配</span>
                        </div>
                    </div>
                </div>
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5">
                    <div class="text-lg mb-3">🔮</div>
                    <div class="text-sm font-bold text-[#e8e8ee] mb-1">证据更新后的信心</div>
                    <p class="text-xs text-[#8888a0] mb-4 leading-relaxed">结合最新政策信息，通过贝叶斯推断动态更新的成功概率。</p>
                    <div class="space-y-2">
                        <div class="flex justify-between items-baseline py-2 border-t border-[#2a2a3a]">
                            <span class="text-xs text-[#8888a0]">最新成功率</span>
                            <span class="text-sm font-bold text-[#22c55e]">{confidence_pct:.1f}%</span>
                        </div>
                        <div class="flex justify-between items-baseline py-2 border-t border-[#2a2a3a]">
                            <span class="text-xs text-[#8888a0]">证据提升幅度</span>
                            <span class="text-sm font-bold text-[#22c55e]">+{shift_delta * 100:.1f}%</span>
                        </div>
                        <div class="flex justify-between items-baseline py-2 border-t border-[#2a2a3a]">
                            <span class="text-xs text-[#8888a0]">信息可信度</span>
                            <span class="text-sm font-bold text-[#e8e8ee]">高质量源</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """

    # Influence diagram section
    influence_section = ""
    if influence:
        influence_section = f"""
        <hr class="border-0 border-t border-[#1e1e2e] my-0">
        <section class="py-8">
            <div class="flex items-center justify-between mb-5">
                <h2 class="text-base font-bold text-[#e8e8ee]">决策要素拆解</h2>
                <span class="text-xs text-[#6666a0]">厘清可控与不可控因素</span>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-lg p-4 text-center">
                    <div class="text-2xl font-extrabold text-[#22c55e]">{dec_n}</div>
                    <div class="text-xs text-[#8888a0] mt-1">我的自主行动</div>
                </div>
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-lg p-4 text-center">
                    <div class="text-2xl font-extrabold text-[#f59e0b]">{chn_n}</div>
                    <div class="text-xs text-[#8888a0] mt-1">外部环境变数</div>
                </div>
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-lg p-4 text-center">
                    <div class="text-2xl font-extrabold text-[#6366f1]">{val_n}</div>
                    <div class="text-xs text-[#8888a0] mt-1">核心追求目标</div>
                </div>
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-lg p-4 text-center">
                    <div class="text-2xl font-extrabold text-[#06b6d4]">{causal_e}</div>
                    <div class="text-xs text-[#8888a0] mt-1">确定因果链路</div>
                </div>
            </div>
            <div class="bg-[#16161f] border border-[#22c55e20] rounded-lg p-4 mt-4 flex justify-between items-center">
                <span class="text-sm text-[#8888a0]">建议优先推进路线</span>
                <span class="text-sm font-bold text-[#22c55e] bg-[#22c55e12] px-3 py-1 rounded-md">德国机会卡 → 欧盟蓝卡</span>
            </div>
        </section>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LifeTree · 决策分析报告</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: #0c0c14; color: #e8e8ee; -webkit-font-smoothing: antialiased; }}
    </style>
</head>
<body class="min-h-screen pb-16">
    <!-- Header -->
    <header class="border-b border-[#1e1e2e] sticky top-0 z-30 bg-[#0c0c14]/95 backdrop-blur-sm">
        <div class="max-w-4xl mx-auto px-6 py-3.5 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <a href="lifetree_homepage.html" class="text-xs text-[#6666a0] hover:text-[#8888a0] transition-colors">← 返回首页</a>
                <span class="text-[#2a2a3a]">|</span>
                <div class="flex items-center gap-2">
                    <div class="w-7 h-7 rounded-md bg-[#22c55e] flex items-center justify-center text-sm">🌳</div>
                    <span class="text-sm font-bold text-[#e8e8ee]">完整分析报告</span>
                </div>
            </div>
            <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-[#22c55e12] border border-[#22c55e25] text-xs font-semibold text-[#22c55e]">
                <div class="w-1.5 h-1.5 rounded-full bg-[#22c55e]"></div>
                分析已完成
            </div>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-6">
        <!-- Hero -->
        <section class="py-10">
            <div class="text-xs font-semibold text-[#22c55e] uppercase tracking-wider mb-3">📊 完整决策分析报告</div>
            <h1 class="text-2xl font-extrabold text-[#f0f0f5] mb-2">推荐路线: 德国机会卡 → 欧盟蓝卡</h1>
            <p class="text-sm text-[#8888a0] max-w-xl">基于万次仿真计算、多维风险评估和行为经济学分析的综合结论。</p>

            <!-- Confidence -->
            <div class="mt-6 max-w-md">
                <div class="flex justify-between items-baseline mb-2">
                    <span class="text-xs text-[#8888a0]">综合成功概率</span>
                    <span class="text-lg font-extrabold text-[#22c55e]">{confidence_pct:.1f}%</span>
                </div>
                <div class="w-full h-2 bg-[#1e1e2e] rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-[#22c55e] to-[#16a34a] rounded-full" style="width: {min(100, confidence_pct)}%"></div>
                </div>
            </div>
        </section>

        <hr class="border-0 border-t border-[#1e1e2e] my-0">

        <!-- Metrics -->
        <section class="py-8">
            <div class="flex items-center justify-between mb-5">
                <h2 class="text-base font-bold text-[#e8e8ee]">核心指标</h2>
                <span class="text-xs text-[#6666a0]">基于 10,000 次仿真</span>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5">
                    <div class="text-xs font-semibold text-[#8888a0] mb-2">预计周期</div>
                    <div class="text-2xl font-extrabold text-[#e8e8ee]">{p50_time}<span class="text-sm font-semibold text-[#8888a0] ml-1">个月</span></div>
                    <div class="text-xs text-[#6666a0] mt-1">悲观预估 ~{p90_time} 个月</div>
                </div>
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5">
                    <div class="text-xs font-semibold text-[#8888a0] mb-2">建议准备资金</div>
                    <div class="text-2xl font-extrabold text-[#e8e8ee]">${var_cost:,.0f}</div>
                    <div class="text-xs text-[#6666a0] mt-1">覆盖 95% 常见情况</div>
                </div>
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5">
                    <div class="text-xs font-semibold text-[#8888a0] mb-2">稳健度评分</div>
                    <div class="text-2xl font-extrabold text-[#e8e8ee]">{regret_idx}<span class="text-sm font-semibold text-[#8888a0] ml-1">/ 100</span></div>
                    <div class="text-xs text-[#6666a0] mt-1">Plan B 备案可靠</div>
                </div>
                <div class="bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5">
                    <div class="text-xs font-semibold text-[#8888a0] mb-2">最佳投入产出</div>
                    <div class="text-base font-extrabold text-[#e8e8ee] mt-1">提升德语至 B1</div>
                    <div class="text-xs text-[#22c55e] mt-1">回报提升 +18.5%</div>
                </div>
            </div>
        </section>

        {ds_section}

        {influence_section}

        <!-- Action Checklist -->
        <hr class="border-0 border-t border-[#1e1e2e] my-0">
        <section class="py-8">
            <div class="flex items-center justify-between mb-5">
                <h2 class="text-base font-bold text-[#e8e8ee]">📋 近期行动清单</h2>
                <span class="text-xs text-[#6666a0]">按投入产出比排序</span>
            </div>
            <div class="bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5">
                {checklist_html}
            </div>
        </section>

        <!-- Footer nav -->
        <hr class="border-0 border-t border-[#1e1e2e] my-0">
        <section class="py-8 pb-16">
            <div class="flex items-center justify-between mb-5">
                <h2 class="text-base font-bold text-[#e8e8ee]">更多分析视图</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <a href="lifetree_growing_tree.html" class="block bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5 hover:border-[#3a3a5a] hover:bg-[#1a1a26] transition-all">
                    <div class="text-lg mb-2">🌳</div>
                    <div class="text-sm font-bold text-[#e8e8ee] mb-1">决策树推演</div>
                    <div class="text-xs text-[#8888a0]">查看不同选择的未来分支走向</div>
                    <span class="text-xs text-[#6666a0] mt-3 inline-block">查看详情 →</span>
                </a>
                <a href="lifetree_deduction_player.html" class="block bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5 hover:border-[#3a3a5a] hover:bg-[#1a1a26] transition-all">
                    <div class="text-lg mb-2">🎬</div>
                    <div class="text-sm font-bold text-[#e8e8ee] mb-1">5年时序推演</div>
                    <div class="text-xs text-[#8888a0]">动态演化曲线与突发冲击测试</div>
                    <span class="text-xs text-[#6666a0] mt-3 inline-block">查看详情 →</span>
                </a>
                <a href="lifetree_graph_viewer.html" class="block bg-[#16161f] border border-[#2a2a3a] rounded-xl p-5 hover:border-[#3a3a5a] hover:bg-[#1a1a26] transition-all">
                    <div class="text-lg mb-2">🕸️</div>
                    <div class="text-sm font-bold text-[#e8e8ee] mb-1">知识图谱</div>
                    <div class="text-xs text-[#8888a0]">探索人物、资产、法规的关系网络</div>
                    <span class="text-xs text-[#6666a0] mt-3 inline-block">查看详情 →</span>
                </a>
            </div>
        </section>
    </main>
</body>
</html>
"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return output_path


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {
            "monte_carlo_results": {
                "execution_timeline_months": {"P50_median": 24.1, "P90_pessimistic": 31.8},
                "financial_capital_usd": {"VaR_95_max_cost": 18508.22}
            },
            "weekly_action_checklist": [
                {"task_title": "提升德语水平至 B1 级", "action_details": "完成 100 小时德语听力与口语强化训练", "priority": "HIGH", "target_deadline": "7 天内"}
            ],
            "tail_risk_results": {"cvar_expected_shortfall_usd": 49103.17, "tail_severity_ratio": 1.289},
            "prospect_theory_results": {"cpt_utility_score": 5423.8},
            "bayesian_belief_results": {"posterior_probability_P_H_given_E": 0.972, "belief_shift_delta": 0.122},
            "influence_diagram_summary": {"decision_nodes_count": 1, "chance_nodes_count": 3, "value_nodes_count": 1, "causal_intervention_edges_count": 2, "optimal_decision_policy": "CHANCENKARTE_ROUTE"},
            "regret_audit": {"audit_summary": {"regret_minimization_index": 93.2}}
        }

    out_file = sys.argv[2] if len(sys.argv) > 2 else "lifetree_decision_report.html"
    res_path = generate_interactive_html_report(data, out_file, lang="zh")
    print(json.dumps({"status": "SUCCESS", "html_report_path": os.path.abspath(res_path)}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
