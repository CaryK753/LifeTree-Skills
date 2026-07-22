#!/usr/bin/env python3
"""
LifeTree Master Aggregator Homepage Generator (All-in-One Portal)
Generates an all-in-one Master Homepage (`lifetree_homepage.html`) that aggregates all 4 LifeTree interactive visual views:
1. 📊 决策推演仪表盘 (Executive Decision Report Dashboard)
2. 🌳 生长决策树全景 (Growing Decision Tree Visualizer)
3. 🎬 5年时序推演演播厅 (5-Year Deduction Scenario Player)
4. 🕸️ 知识土壤拓扑查看器 (Knowledge Graph Viewer)
"""

import os
import sys
import json
from typing import Dict, Any

def generate_homepage_html(pipeline_data: Dict[str, Any], output_path: str, lang: str = "zh") -> str:
    """
    Generates a single master aggregator homepage HTML file with seamless tab navigation and responsive design.
    """
    is_zh = (lang == "zh")

    mc = pipeline_data.get("monte_carlo_results", {})
    p50_time = mc.get("execution_timeline_months", {}).get("P50_median", 24)
    var_cost = mc.get("financial_capital_usd", {}).get("VaR_95_max_cost", 18508)
    cvar_cost = pipeline_data.get("tail_risk_results", {}).get("cvar_expected_shortfall_usd", 49103)

    title_text = "LifeTree 个人决策智能总控主页" if is_zh else "LifeTree Decision Intelligence Master Portal"

    html_content = f"""<!DOCTYPE html>
<html lang="{ 'zh-CN' if is_zh else 'en' }" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', 'Inter', sans-serif; background-color: #07090e; color: #f8fafc; margin: 0; overflow: hidden; }}
        .glass-panel {{ background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        .glow-border {{ box-shadow: 0 0 25px -5px rgba(16, 185, 129, 0.15); }}
        .gradient-text {{ background: linear-gradient(135deg, #34d399 0%, #10b981 50%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .tab-btn {{ transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); }}
        .tab-btn.active {{ background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(6, 182, 212, 0.2) 100%); border-color: rgba(52, 211, 153, 0.4); color: #ffffff; box-shadow: 0 4px 20px -2px rgba(16, 185, 129, 0.25); }}
    </style>
</head>
<body class="h-screen flex flex-col">
    <!-- Top Master Control Header -->
    <header class="z-30 border-b border-slate-800 bg-slate-950/80 backdrop-blur-xl px-6 py-3.5 flex items-center justify-between shadow-2xl">
        <!-- Brand Logo & Live Ticker -->
        <div class="flex items-center gap-6">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center text-xl shadow-lg shadow-emerald-500/20">
                    🌳
                </div>
                <div>
                    <h1 class="text-lg font-extrabold text-white tracking-tight flex items-center gap-2">
                        LifeTree <span class="gradient-text">{ '决策智能全景中心' if is_zh else 'Decision Portal' }</span>
                    </h1>
                    <p class="text-xs text-slate-400">{ '以对象为中心的个人决策操作系统 · 4合1 聚合入口' if is_zh else 'Personal Decision Intelligence Operating System (Life OS)' }</p>
                </div>
            </div>

            <!-- KPI Ticker Pills -->
            <div class="hidden xl:flex items-center gap-3 pl-6 border-l border-slate-800 text-xs">
                <div class="px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center gap-2">
                    <span class="text-slate-400">{ '预期周期:' if is_zh else 'Timeline:' }</span>
                    <span class="font-bold text-emerald-400 font-mono">{p50_time} { '个月' if is_zh else 'm' }</span>
                </div>
                <div class="px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center gap-2">
                    <span class="text-slate-400">{ '最坏保障资金:' if is_zh else 'CVaR Shortfall:' }</span>
                    <span class="font-bold text-rose-400 font-mono">${cvar_cost:,.0f}</span>
                </div>
                <div class="px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    <span class="font-semibold text-emerald-300">{ '核心推荐: 提升德语至 B1' if is_zh else 'Top Action: B1 German' }</span>
                </div>
            </div>
        </div>

        <!-- Master Tab Navigation -->
        <nav class="flex items-center gap-2 p-1.5 rounded-2xl bg-slate-900/90 border border-slate-800">
            <button onclick="switchTab('report')" id="tab-report" class="tab-btn active px-4 py-2 text-xs font-bold rounded-xl border border-transparent text-slate-400 hover:text-white flex items-center gap-2">
                <span>📊</span>
                <span>{ '决策推演仪表盘' if is_zh else 'Executive Dashboard' }</span>
            </button>
            <button onclick="switchTab('tree')" id="tab-tree" class="tab-btn px-4 py-2 text-xs font-bold rounded-xl border border-transparent text-slate-400 hover:text-white flex items-center gap-2">
                <span>🌳</span>
                <span>{ '生长决策树全景' if is_zh else 'Growing Decision Tree' }</span>
            </button>
            <button onclick="switchTab('player')" id="tab-player" class="tab-btn px-4 py-2 text-xs font-bold rounded-xl border border-transparent text-slate-400 hover:text-white flex items-center gap-2">
                <span>🎬</span>
                <span>{ '5年时序演播厅' if is_zh else 'Deduction Player' }</span>
            </button>
            <button onclick="switchTab('graph')" id="tab-graph" class="tab-btn px-4 py-2 text-xs font-bold rounded-xl border border-transparent text-slate-400 hover:text-white flex items-center gap-2">
                <span>🕸️</span>
                <span>{ '知识土壤图谱' if is_zh else 'Knowledge Graph' }</span>
            </button>
        </nav>
    </header>

    <!-- Main Viewport Container (Seamless Dynamic iFrames) -->
    <main class="flex-1 relative bg-slate-950">
        <iframe id="frame-report" src="lifetree_decision_report.html" class="w-full h-full border-none absolute inset-0 block"></iframe>
        <iframe id="frame-tree" src="lifetree_growing_tree.html" class="w-full h-full border-none absolute inset-0 hidden"></iframe>
        <iframe id="frame-player" src="lifetree_deduction_player.html" class="w-full h-full border-none absolute inset-0 hidden"></iframe>
        <iframe id="frame-graph" src="lifetree_graph_viewer.html" class="w-full h-full border-none absolute inset-0 hidden"></iframe>
    </main>

    <script>
        function switchTab(tabKey) {{
            // Deactivate all tabs
            ['report', 'tree', 'player', 'graph'].forEach(key => {{
                document.getElementById('tab-' + key).classList.remove('active');
                document.getElementById('frame-' + key).classList.add('hidden');
                document.getElementById('frame-' + key).classList.remove('block');
            }});

            // Activate target tab
            document.getElementById('tab-' + tabKey).classList.add('active');
            document.getElementById('frame-' + tabKey).classList.remove('hidden');
            document.getElementById('frame-' + tabKey).classList.add('block');
        }}
    </script>
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
                "execution_timeline_months": {"P50_median": 24.1},
                "financial_capital_usd": {"VaR_95_max_cost": 18508.22}
            },
            "tail_risk_results": {"cvar_expected_shortfall_usd": 49103.17}
        }

    out_file = sys.argv[2] if len(sys.argv) > 2 else "lifetree_homepage.html"
    res_path = generate_homepage_html(data, out_file, lang="zh")
    print(json.dumps({"status": "SUCCESS", "homepage_html_path": os.path.abspath(res_path)}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
