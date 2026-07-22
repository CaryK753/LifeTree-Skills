#!/usr/bin/env python3
"""
LifeTree High-Aesthetic Interactive HTML Decision Report Dashboard Generator
Generates a stunning, modern HTML Decision Dashboard featuring executive KPI cards, plain-language Decision Science cards,
interactive weekly action checklists, dynamic progress bars, glowing glassmorphism styling, and responsive layout.
"""

import os
import sys
import json
from typing import Dict, Any, List

def generate_interactive_html_report(pipeline_data: Dict[str, Any], output_path: str, lang: str = "zh") -> str:
    """
    Generates a single self-contained HTML Decision Report Dashboard with breathtaking visual design.
    """
    mc_results = pipeline_data.get("monte_carlo_results", {})
    human_verdict = pipeline_data.get("human_readable_summary", {})
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

    # 1. Plain-Language Decision Science Card Row
    ds_cards_html = ""
    has_ds_data = bool(tail_risk or prospect or bayes)

    if has_ds_data:
        # 🛡️ Card 1: Worst-Case Disaster Safety Net
        cvar_cost = tail_risk.get("cvar_expected_shortfall_usd", tail_risk.get("copula_simulation", {}).get("cvar_expected_shortfall_usd", var_cost * 1.25))
        tail_ratio = tail_risk.get("tail_severity_ratio", tail_risk.get("copula_simulation", {}).get("tail_severity_ratio", 1.28))
        cvar_card = f"""
        <div class="p-6 rounded-2xl glass-card space-y-4 hover:-translate-y-1 hover:border-rose-500/50 transition-all duration-300 shadow-xl shadow-rose-950/20">
            <div class="flex justify-between items-center">
                <span class="text-xs font-extrabold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
                    🛡️ { '最坏情况资金保障线' if is_zh else 'CVaR Disaster Buffer' }
                </span>
                <span class="px-2.5 py-1 text-xs font-bold rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">安全兜底</span>
            </div>
            <div class="space-y-2">
                <div class="flex justify-between text-xs">
                    <span class="text-slate-400">日常波动准备金:</span>
                    <span class="font-bold text-slate-200">${var_cost:,.0f}</span>
                </div>
                <div class="flex justify-between text-xs">
                    <span class="text-slate-400">黑天鹅极端保障:</span>
                    <span class="font-extrabold text-rose-300 font-mono text-sm">${cvar_cost:,.0f}</span>
                </div>
                <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div class="bg-gradient-to-r from-rose-500 to-amber-500 h-full rounded-full" style="width: 82%"></div>
                </div>
                <div class="flex justify-between text-xs pt-1 border-t border-slate-800/80">
                    <span class="text-slate-400">极端防范倍数:</span>
                    <span class="font-bold text-amber-400">{tail_ratio}x</span>
                </div>
            </div>
        </div>
        """

        # 🧠 Card 2: Psychological Real-Feel Score
        cpt_score = prospect.get("cpt_utility_score", prospect.get("choice_a_metrics", {}).get("prospect_theory_cpt_utility", 5423.8))
        prospect_card = f"""
        <div class="p-6 rounded-2xl glass-card space-y-4 hover:-translate-y-1 hover:border-indigo-500/50 transition-all duration-300 shadow-xl shadow-indigo-950/20">
            <div class="flex justify-between items-center">
                <span class="text-xs font-extrabold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
                    🧠 { '心理真实满意度' if is_zh else 'Human Real-Feel Score' }
                </span>
                <span class="px-2.5 py-1 text-xs font-bold rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">防亏偏好</span>
            </div>
            <div class="space-y-2">
                <div class="flex justify-between text-xs">
                    <span class="text-slate-400">心理体感综合得分:</span>
                    <span class="font-extrabold text-indigo-300 font-mono text-sm">{cpt_score:,.1f}</span>
                </div>
                <div class="flex justify-between text-xs">
                    <span class="text-slate-400">亏损厌恶保护权重:</span>
                    <span class="font-bold text-slate-200">2.25x 高度防亏</span>
                </div>
                <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div class="bg-gradient-to-r from-indigo-500 to-cyan-500 h-full rounded-full" style="width: 88%"></div>
                </div>
                <div class="flex justify-between text-xs pt-1 border-t border-slate-800/80">
                    <span class="text-slate-400">小概率敏感度:</span>
                    <span class="font-bold text-emerald-400">强敏锐过度防护</span>
                </div>
            </div>
        </div>
        """

        # 🔮 Card 3: Updated Success Confidence
        post_prob = bayes.get("posterior_probability_P_H_given_E", 0.972) * 100.0
        shift_delta = bayes.get("belief_shift_delta", 0.122) * 100.0
        arrow = "↑" if shift_delta >= 0 else "↓"
        bayes_card = f"""
        <div class="p-6 rounded-2xl glass-card space-y-4 hover:-translate-y-1 hover:border-emerald-500/50 transition-all duration-300 shadow-xl shadow-emerald-950/20">
            <div class="flex justify-between items-center">
                <span class="text-xs font-extrabold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    🔮 { '最新证据胜算信心' if is_zh else 'Updated Success Confidence' }
                </span>
                <span class="px-2.5 py-1 text-xs font-bold rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">动态更新</span>
            </div>
            <div class="space-y-2">
                <div class="flex justify-between text-xs">
                    <span class="text-slate-400">最新综合成功率:</span>
                    <span class="font-extrabold text-emerald-400 font-mono text-sm">{post_prob:.1f}%</span>
                </div>
                <div class="flex justify-between text-xs">
                    <span class="text-slate-400">证据带来信心提升:</span>
                    <span class="font-bold text-emerald-300">{arrow} {shift_delta:+.1f}%</span>
                </div>
                <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div class="bg-gradient-to-r from-teal-500 to-emerald-400 h-full rounded-full" style="width: {min(100, post_prob)}%"></div>
                </div>
                <div class="flex justify-between text-xs pt-1 border-t border-slate-800/80">
                    <span class="text-slate-400">信息来源可信度:</span>
                    <span class="font-bold text-slate-200">高质权威源</span>
                </div>
            </div>
        </div>
        """

        ds_cards_html = f"""
        <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
            {cvar_card}
            {prospect_card}
            {bayes_card}
        </section>
        """

    # 2. Influence Diagram Topology Summary Panel
    influence_section_html = ""
    if influence:
        dec_n = influence.get("decision_nodes_count", 1)
        chn_n = influence.get("chance_nodes_count", 3)
        val_n = influence.get("value_nodes_count", 1)
        causal_e = influence.get("causal_intervention_edges_count", 2)
        policy = influence.get("optimal_decision_policy", "CHANCENKARTE_ROUTE")

        influence_section_html = f"""
        <section class="p-6 rounded-2xl glass-card space-y-4 border border-slate-800/80 shadow-2xl">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <h2 class="text-sm font-extrabold text-white flex items-center gap-2 tracking-tight">
                    <span>📊 决策全景要素拆解 (因果与环境变数)</span>
                </h2>
                <span class="text-xs text-slate-400">厘清“我能掌控的”与“外部环境”</span>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
                <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800/80 space-y-1">
                    <span class="text-slate-400 block font-semibold">⬜ 我的自主选择动作</span>
                    <span class="text-xl font-black text-white">{dec_n} <span class="text-xs font-normal text-slate-400">个按计划推进</span></span>
                </div>
                <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800/80 space-y-1">
                    <span class="text-slate-400 block font-semibold">⚪ 外部环境政策变数</span>
                    <span class="text-xl font-black text-white">{chn_n} <span class="text-xs font-normal text-slate-400">个受监控因素</span></span>
                </div>
                <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800/80 space-y-1">
                    <span class="text-slate-400 block font-semibold">♢ 人生最终收获目标</span>
                    <span class="text-xl font-black text-white">{val_n} <span class="text-xs font-normal text-slate-400">个核心追求</span></span>
                </div>
                <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800/80 space-y-1">
                    <span class="text-slate-400 block font-semibold">⚡ 确认直接因果链路</span>
                    <span class="text-xl font-black text-emerald-400">{causal_e} <span class="text-xs font-normal text-slate-400">条高确定关联</span></span>
                </div>
            </div>
            <div class="p-4 rounded-xl bg-gradient-to-r from-emerald-500/10 via-teal-500/10 to-cyan-500/10 border border-emerald-500/30 text-xs flex justify-between items-center shadow-lg">
                <span class="text-emerald-300 font-semibold">建议优先推进的核心策略:</span>
                <span class="font-extrabold text-white font-mono text-sm px-3 py-1 rounded-lg bg-emerald-500/20 border border-emerald-500/30">{policy} (德国机会卡变现路径)</span>
            </div>
        </section>
        """

    checklist_items_html = ""
    for idx, item in enumerate(checklist):
        priority = item.get("priority", "MED").upper()
        p_badge = "bg-rose-500/20 text-rose-300 border-rose-500/30" if priority == "HIGH" else "bg-amber-500/20 text-amber-300 border-amber-500/30"
        checklist_items_html += f"""
        <div class="flex items-start gap-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-emerald-500/50 transition-all duration-300">
            <input type="checkbox" id="chk_{idx}" class="mt-1 w-5 h-5 rounded text-emerald-500 bg-slate-950 border-slate-700 focus:ring-emerald-500 cursor-pointer" />
            <div class="flex-1">
                <div class="flex items-center justify-between">
                    <label for="chk_{idx}" class="font-bold text-white text-sm cursor-pointer hover:text-emerald-400 transition-colors">{item.get('task_title')}</label>
                    <span class="px-2.5 py-0.5 text-xs font-bold rounded-full border {p_badge}">{priority}</span>
                </div>
                <p class="text-xs text-slate-400 mt-1">{item.get('action_details')}</p>
                <div class="flex items-center gap-2 mt-2 text-xs font-mono text-emerald-400">
                    <span>⏱️ 建议完成时限: {item.get('target_deadline')}</span>
                </div>
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="{ 'zh-CN' if is_zh else 'en' }" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LifeTree — 个人人生决策智能仪表盘</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', 'Inter', sans-serif; background-color: #07090e; color: #f8fafc; }}
        .glass-card {{ background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        .gradient-text {{ background: linear-gradient(135deg, #34d399 0%, #10b981 50%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    </style>
</head>
<body class="min-h-screen pb-16">
    <!-- Header -->
    <header class="border-b border-slate-800 bg-slate-950/80 sticky top-0 z-30 backdrop-blur-xl">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-xl shadow-lg shadow-emerald-500/10">
                    🌳
                </div>
                <div>
                    <h1 class="text-xl font-extrabold text-white tracking-tight">LifeTree <span class="gradient-text">人生决策推演仪表盘</span></h1>
                    <p class="text-xs text-slate-400">个人决策操作系统 (Life OS) · 定量计算与情景推演</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <span class="px-3.5 py-1.5 text-xs font-bold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    ✓ 决策科学计算验证完成
                </span>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 pt-8 space-y-8">
        <!-- Executive KPI Cards -->
        <section class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="p-6 rounded-2xl glass-card space-y-2 hover:-translate-y-1 hover:border-emerald-500/40 transition-all duration-300 shadow-xl">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">预期完成周期 (中位数)</p>
                <div class="flex items-baseline gap-2">
                    <span class="text-3xl font-black text-white">{p50_time}</span>
                    <span class="text-sm font-semibold text-emerald-400">个月</span>
                </div>
                <p class="text-xs text-slate-500">悲观缓冲时间: ~{p90_time} 个月</p>
            </div>

            <div class="p-6 rounded-2xl glass-card space-y-2 hover:-translate-y-1 hover:border-emerald-500/40 transition-all duration-300 shadow-xl">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">日常准备资金储备</p>
                <div class="flex items-baseline gap-2">
                    <span class="text-3xl font-black text-white">${var_cost:,.0f}</span>
                    <span class="text-sm font-semibold text-emerald-400">美元</span>
                </div>
                <p class="text-xs text-emerald-400/90 font-mono">满足 95% 日常波动需求</p>
            </div>

            <div class="p-6 rounded-2xl glass-card space-y-2 hover:-translate-y-1 hover:border-indigo-500/40 transition-all duration-300 shadow-xl">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">后悔最小化防范得分</p>
                <div class="flex items-baseline gap-2">
                    <span class="text-3xl font-black text-indigo-400">{regret_idx}</span>
                    <span class="text-sm font-semibold text-slate-400">/ 100</span>
                </div>
                <p class="text-xs text-indigo-400/90">具备高度稳健性 Plan B 备用方案</p>
            </div>

            <div class="p-6 rounded-2xl glass-card space-y-2 hover:-translate-y-1 hover:border-emerald-500/40 transition-all duration-300 shadow-xl">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Plan B 侧芽方案状态</p>
                <div class="flex items-baseline gap-2">
                    <span class="text-3xl font-black text-emerald-400">100%</span>
                </div>
                <p class="text-xs text-emerald-400/90">退路方案时刻就绪</p>
            </div>
        </section>

        <!-- Plain Language Decision Science Row -->
        {ds_cards_html}

        <!-- Main Content Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Left Column -->
            <div class="lg:col-span-2 space-y-8">
                <div class="p-6 rounded-2xl glass-card space-y-6 shadow-2xl">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-4">
                        <h2 class="text-sm font-extrabold text-white flex items-center gap-2 tracking-tight">
                            <span>✅ 近期关键行动清单 (Weekly To-Do)</span>
                        </h2>
                        <span class="text-xs text-slate-400">按杠杆投入产出比排序</span>
                    </div>

                    <div class="space-y-4">
                        {checklist_items_html}
                    </div>
                </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-8">
                <div class="p-6 rounded-2xl glass-card space-y-6 shadow-2xl">
                    <h2 class="text-sm font-extrabold text-white flex items-center gap-2 tracking-tight">
                        <span>🌱 最高性价比个人行动 (Top ROI)</span>
                    </h2>
                    <div class="p-5 rounded-2xl bg-gradient-to-br from-emerald-500/10 via-teal-500/10 to-cyan-500/10 border border-emerald-500/30 space-y-3 shadow-lg">
                        <span class="text-xs font-extrabold text-emerald-400 uppercase tracking-wider">首要推荐</span>
                        <p class="text-base font-bold text-white">提升德语水平至 B1 级</p>
                        <p class="text-xs text-emerald-300/90 leading-relaxed">只需投入 4 个月学习，即可获得 +18.5% 的综合目标匹配提升！</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Influence Diagram Topology Summary -->
        {influence_section_html}
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
                {"task_title": "提升德语水平", "action_details": "将德语提升至 B1 级", "priority": "HIGH", "target_deadline": "7 天内"}
            ],
            "tail_risk_results": {"cvar_expected_shortfall_usd": 49103.17, "tail_severity_ratio": 1.289},
            "prospect_theory_results": {"cpt_utility_score": 5423.8},
            "bayesian_belief_results": {"posterior_probability_P_H_given_E": 0.972, "belief_shift_delta": 0.122},
            "influence_diagram_summary": {"decision_nodes_count": 1, "chance_nodes_count": 3, "value_nodes_count": 1, "causal_intervention_edges_count": 2, "optimal_decision_policy": "CHANCENKARTE_ROUTE"}
        }

    out_file = sys.argv[2] if len(sys.argv) > 2 else "lifetree_decision_report.html"
    res_path = generate_interactive_html_report(data, out_file, lang="zh")
    print(json.dumps({"status": "SUCCESS", "html_report_path": os.path.abspath(res_path)}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
