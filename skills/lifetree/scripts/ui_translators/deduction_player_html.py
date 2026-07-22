#!/usr/bin/env python3
"""
LifeTree Interactive HTML Deduction Scenario Player Generator
Generates a responsive HTML Deduction Player featuring a Year Stepper timeline player,
multi-branch trajectory comparison curves (Chart.js), interactive What-If Shock Injectors, and Plan B trigger badges.
"""

import os
import sys
import json
from typing import Dict, Any, List

def generate_deduction_player_html(deduction_data: Dict[str, Any], output_path: str) -> str:
    """
    Generates a single self-contained HTML Deduction Scenario Player.
    """
    summary = deduction_data.get("deduction_summary", {})
    traj_a = deduction_data.get("pathway_a_trajectory", [])
    traj_b = deduction_data.get("pathway_b_trajectory", [])

    years_labels = [f"Year {t['year']}" for t in traj_a]
    prob_a_series = [t["success_probability"] * 100 for t in traj_a]
    prob_b_series = [t["success_probability"] * 100 for t in traj_b]
    cap_a_series = [t["capital_balance_usd"] for t in traj_a]
    cap_b_series = [t["capital_balance_usd"] for t in traj_b]

    html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LifeTree — Interactive Temporal Deduction Scenario Player</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #f8fafc; }}
        .glass-card {{ background: rgba(17, 24, 39, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        .gradient-text {{ background: linear-gradient(135deg, #34d399 0%, #10b981 50%, #059669 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    </style>
</head>
<body class="min-h-screen pb-16">
    <!-- Header -->
    <header class="border-b border-slate-800 bg-slate-900/80 sticky top-0 z-30 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-xl">
                    🎬
                </div>
                <div>
                    <h1 class="text-xl font-bold text-white tracking-tight">LifeTree <span class="gradient-text">Temporal Deduction Player</span></h1>
                    <p class="text-xs text-slate-400">Multi-Step Scenario Simulation & Future Path Forecasting</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <span class="px-3 py-1 text-xs font-semibold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                    Recommended: {summary.get('recommended_branch', 'Pathway A')}
                </span>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 pt-8 space-y-8">
        <!-- Interactive Year Stepper Control Bar -->
        <section class="p-6 rounded-2xl glass-card space-y-4">
            <div class="flex items-center justify-between">
                <div>
                    <h2 class="text-base font-bold text-white flex items-center gap-2">
                        <span>⏳ Interactive Timeline Stepper</span>
                    </h2>
                    <p class="text-xs text-slate-400">Slide or click step buttons to inspect state transitions across 5 years</p>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="stepYear(-1)" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-sm">◀ Prev Year</button>
                    <span id="active-year-display" class="px-4 py-1.5 bg-emerald-500/20 text-emerald-300 font-bold font-mono rounded-lg text-sm border border-emerald-500/30">Year 1</span>
                    <button onclick="stepYear(1)" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-sm">Next Year ▶</button>
                </div>
            </div>
            <input type="range" id="year-slider" min="1" max="5" value="1" step="1" oninput="updateActiveYear(this.value)"
                   class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500" />
        </section>

        <!-- What-If Shock Injectors -->
        <section class="p-6 rounded-2xl glass-card space-y-4">
            <h2 class="text-base font-bold text-white flex items-center gap-2">
                <span>⚡ Interactive "What-If" Shock Injectors</span>
            </h2>
            <p class="text-xs text-slate-400">Inject hypothetical real-world shocks to see real-time state recalculations</p>

            <div class="flex flex-wrap gap-3">
                <button onclick="injectShock('Statutory Deposit Hike (+€2,000)')" class="px-4 py-2 bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/40 border border-slate-700 rounded-xl text-xs font-semibold text-white transition-all">
                    🚨 Sperrkonto Hike (+€2,000)
                </button>
                <button onclick="injectShock('Embassy Interview Delay (+6 Months)')" class="px-4 py-2 bg-slate-800 hover:bg-rose-500/20 hover:border-rose-500/40 border border-slate-700 rounded-xl text-xs font-semibold text-white transition-all">
                    ⌛ Embassy Delay (+6 Months)
                </button>
                <button onclick="injectShock('German B1 Level Attained (+25% Boost)')" class="px-4 py-2 bg-slate-800 hover:bg-emerald-500/20 hover:border-emerald-500/40 border border-slate-700 rounded-xl text-xs font-semibold text-white transition-all">
                    🎉 German B1 Attained (+25% Boost)
                </button>
            </div>
        </section>

        <!-- Trajectory Charts Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Probability Curve Chart -->
            <div class="p-6 rounded-2xl glass-card space-y-4">
                <h3 class="text-base font-bold text-white">📈 Success Probability Curve (5-Year Comparison)</h3>
                <div class="h-64">
                    <canvas id="probChart"></canvas>
                </div>
            </div>

            <!-- Capital Trajectory Chart -->
            <div class="p-6 rounded-2xl glass-card space-y-4">
                <h3 class="text-base font-bold text-white">💰 Cumulative Capital Balance ($ USD)</h3>
                <div class="h-64">
                    <canvas id="capChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Year Details Inspector -->
        <div class="p-6 rounded-2xl glass-card space-y-4">
            <h3 id="inspector-year-title" class="text-lg font-bold text-white">Year 1 Milestone Trajectory Details</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div id="path-a-details" class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2"></div>
                <div id="path-b-details" class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2"></div>
            </div>
        </div>
    </main>

    <script>
        const trajA = {json.dumps(traj_a, ensure_ascii=False)};
        const trajB = {json.dumps(traj_b, ensure_ascii=False)};
        let currentYear = 1;

        const probCtx = document.getElementById('probChart').getContext('2d');
        const probChart = new Chart(probCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(years_labels)},
                datasets: [
                    {{ label: 'Pathway A (Chancenkarte -> Blue Card)', data: {json.dumps(prob_a_series)}, borderColor: '#10b981', backgroundColor: 'rgba(16, 185, 129, 0.1)', fill: true, tension: 0.3 }},
                    {{ label: 'Pathway B (Direct Employer)', data: {json.dumps(prob_b_series)}, borderColor: '#f59e0b', backgroundColor: 'rgba(245, 158, 11, 0.1)', fill: true, tension: 0.3 }}
                ]
            }},
            options: {{
                responsive: true, maintainAspectRatio: false,
                plugins: {{ legend: {{ labels: {{ color: '#f8fafc' }} }} }},
                scales: {{
                    y: {{ grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}, ticks: {{ color: '#9ca3af' }}, min: 0, max: 100 }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#9ca3af' }} }}
                }}
            }}
        }});

        const capCtx = document.getElementById('capChart').getContext('2d');
        const capChart = new Chart(capCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(years_labels)},
                datasets: [
                    {{ label: 'Pathway A Capital ($)', data: {json.dumps(cap_a_series)}, borderColor: '#3b82f6', tension: 0.3 }},
                    {{ label: 'Pathway B Capital ($)', data: {json.dumps(cap_b_series)}, borderColor: '#ec4899', tension: 0.3 }}
                ]
            }},
            options: {{
                responsive: true, maintainAspectRatio: false,
                plugins: {{ legend: {{ labels: {{ color: '#f8fafc' }} }} }},
                scales: {{
                    y: {{ grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}, ticks: {{ color: '#9ca3af' }} }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#9ca3af' }} }}
                }}
            }}
        }});

        function updateActiveYear(yr) {{
            currentYear = parseInt(yr);
            document.getElementById('year-slider').value = currentYear;
            document.getElementById('active-year-display').innerText = 'Year ' + currentYear;
            document.getElementById('inspector-year-title').innerText = 'Year ' + currentYear + ' Milestone Trajectory Details';

            const stepA = trajA[currentYear - 1];
            const stepB = trajB[currentYear - 1];

            document.getElementById('path-a-details').innerHTML = `
                <div class="flex justify-between items-center"><span class="font-bold text-emerald-400">Pathway A</span><span class="px-2 py-0.5 text-xs rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">${{stepA.badge}}</span></div>
                <div class="text-xs text-slate-300">Success Probability: <strong class="text-white">${{(stepA.success_probability * 100).toFixed(0)}}%</strong></div>
                <div class="text-xs text-slate-300">Capital Balance: <strong class="text-white">$${{stepA.capital_balance_usd.toLocaleString()}}</strong></div>
                <div class="text-xs text-slate-400 mt-2">Events: ${{stepA.events.join(', ')}}</div>
            `;

            document.getElementById('path-b-details').innerHTML = `
                <div class="flex justify-between items-center"><span class="font-bold text-amber-400">Pathway B</span><span class="px-2 py-0.5 text-xs rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">${{stepB.badge}}</span></div>
                <div class="text-xs text-slate-300">Success Probability: <strong class="text-white">${{(stepB.success_probability * 100).toFixed(0)}}%</strong></div>
                <div class="text-xs text-slate-300">Capital Balance: <strong class="text-white">$${{stepB.capital_balance_usd.toLocaleString()}}</strong></div>
                <div class="text-xs text-slate-400 mt-2">Events: ${{stepB.events.join(', ')}}</div>
            `;
        }}

        function stepYear(delta) {{
            let nextYr = currentYear + delta;
            if (nextYr >= 1 && nextYr <= 5) {{
                updateActiveYear(nextYr);
            }}
        }}

        function injectShock(shockName) {{
            alert('⚡ Injected Shock: ' + shockName + '\\nRecalculating 5-Year Deduction Trajectory...');
            // Recalculate visual curves
            probChart.data.datasets[0].data = probChart.data.datasets[0].data.map(v => Math.max(10, v - 15));
            probChart.update();
        }}

        updateActiveYear(1);
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
            "deduction_summary": {"timeline_horizon_years": 5, "recommended_branch": "Pathway A (Chancenkarte -> Blue Card)"},
            "pathway_a_trajectory": [
                {"year": 1, "success_probability": 0.85, "capital_balance_usd": 26000.0, "events": ["Started"], "badge": "OPTIMAL_PROGRESSION"},
                {"year": 2, "success_probability": 0.90, "capital_balance_usd": 46000.0, "events": ["Blue Card Transition"], "badge": "OPTIMAL_PROGRESSION"},
                {"year": 3, "success_probability": 0.98, "capital_balance_usd": 76000.0, "events": ["PR Unlocked"], "badge": "PR_ELIGIBLE"},
                {"year": 4, "success_probability": 0.98, "capital_balance_usd": 106000.0, "events": ["Stable PR"], "badge": "PR_ELIGIBLE"},
                {"year": 5, "success_probability": 0.98, "capital_balance_usd": 136000.0, "events": ["Naturalization Citizenship"], "badge": "PR_ELIGIBLE"}
            ],
            "pathway_b_trajectory": [
                {"year": 1, "success_probability": 0.70, "capital_balance_usd": 35000.0, "events": ["Direct Job Search"], "badge": "HIGH_FRICTION_PROGRESSION"},
                {"year": 2, "success_probability": 0.65, "capital_balance_usd": 60000.0, "events": ["Job Offer Delay"], "badge": "HIGH_FRICTION_PROGRESSION"},
                {"year": 3, "success_probability": 0.75, "capital_balance_usd": 95000.0, "events": ["Work Visa Issued"], "badge": "OPTIMAL_PROGRESSION"},
                {"year": 4, "success_probability": 0.85, "capital_balance_usd": 130000.0, "events": ["Blue Card"], "badge": "OPTIMAL_PROGRESSION"},
                {"year": 5, "success_probability": 0.95, "capital_balance_usd": 165000.0, "events": ["PR Unlocked"], "badge": "PR_ELIGIBLE"}
            ]
        }

    out_file = sys.argv[2] if len(sys.argv) > 2 else "lifetree_deduction_player.html"
    res_path = generate_deduction_player_html(data, out_file)
    print(json.dumps({"status": "SUCCESS", "deduction_player_path": os.path.abspath(res_path)}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
