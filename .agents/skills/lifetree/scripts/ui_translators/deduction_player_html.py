#!/usr/bin/env python3
"""
LifeTree Deduction Mode Interactive Timeline Player Generator (i18n Enhanced)
Generates an interactive 5-Year Temporal Deduction Player featuring Chart.js probability & capital curves,
What-If shock injectors, and responsive multi-language (i18n) controls.
"""

import os
import sys
import json
from typing import Dict, Any, List

def generate_deduction_player_html(deduction_data: Dict[str, Any], output_path: str, lang: str = "zh") -> str:
    """
    Generates a single self-contained HTML file displaying an interactive 5-year deduction timeline player.
    """
    proj = deduction_data.get("timeline_projection", [])
    is_zh = (lang == "zh")

    years = [p.get("year", 2026 + i) for i, p in enumerate(proj)] or [2026, 2027, 2028, 2029, 2030]
    capital_curve = [p.get("net_worth_usd", 40000 + i * 15000) for i, p in enumerate(proj)] or [40000, 55000, 75000, 105000, 140000]
    confidence_curve = [p.get("confidence_score", 0.95 - i * 0.03) * 100 for i, p in enumerate(proj)] or [95, 92, 88, 85, 80]

    title_text = "LifeTree 5年时序推演演播厅" if is_zh else "LifeTree 5-Year Temporal Deduction Player"
    subtitle_text = "动态推演播放 · 突发冲击测试 · 资金与胜算演化曲线" if is_zh else "Dynamic Timeline Player · What-If Shock Injector · Capital & Confidence Curves"
    play_btn = "▶ 播放 5 年推演" if is_zh else "▶ Play 5-Year Deduction"
    shock_btn = "⚡ 注入突发通胀/规则变更冲击" if is_zh else "⚡ Inject What-If Macro Shock"

    label_cap = "个人净资金储备 ($)" if is_zh else "Capital Balance ($)"
    label_conf = "胜算信心度 (%)" if is_zh else "Confidence (%)"

    html_content = f"""<!DOCTYPE html>
<html lang="{ 'zh-CN' if is_zh else 'en' }" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LifeTree — {title_text}</title>
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
    <header class="border-b border-slate-800 bg-slate-900/60 sticky top-0 z-30 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-xl">
                    🎬
                </div>
                <div>
                    <h1 class="text-xl font-bold text-white tracking-tight">LifeTree <span class="gradient-text">{ '时序推演演播厅' if is_zh else 'Deduction Player' }</span></h1>
                    <p class="text-xs text-slate-400">{subtitle_text}</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <button onclick="playTimelineAnimation()" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-emerald-900/30 transition-all flex items-center gap-2">
                    <span>{play_btn}</span>
                </button>
                <button onclick="injectMacroShock()" class="px-4 py-2.5 bg-rose-600/80 hover:bg-rose-500 text-white font-semibold text-xs rounded-xl border border-rose-500/40 transition-all">
                    {shock_btn}
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 pt-8 space-y-8">
        <!-- Control Player Bar -->
        <section class="p-6 rounded-2xl glass-card space-y-4">
            <div class="flex justify-between items-center text-xs text-slate-400 font-mono">
                <span>{ '推演起止年份: 2026' if is_zh else 'Start: 2026' }</span>
                <span id="current-year-label" class="text-base font-bold text-emerald-400">{ '当前播放年份: 2026' if is_zh else 'Current Year: 2026' }</span>
                <span>{ '终点: 2030' if is_zh else 'Target: 2030' }</span>
            </div>
            <input type="range" id="timelineSlider" min="0" max="4" value="0" step="1" oninput="updateYearView(this.value)" class="w-full h-3 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500" />
        </section>

        <!-- Charts Grid -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="p-6 rounded-2xl glass-card space-y-4">
                <h2 class="text-sm font-bold text-white flex items-center gap-2">
                    <span>💰 { '个人资产资金演化曲线 ($)' if is_zh else 'Capital Balance Growth ($)' }</span>
                </h2>
                <div class="h-64 relative">
                    <canvas id="capitalChart"></canvas>
                </div>
            </div>

            <div class="p-6 rounded-2xl glass-card space-y-4">
                <h2 class="text-sm font-bold text-white flex items-center gap-2">
                    <span>🛡️ { '决策信心与胜算演化 (%)' if is_zh else 'Decision Confidence (%)' }</span>
                </h2>
                <div class="h-64 relative">
                    <canvas id="confidenceChart"></canvas>
                </div>
            </div>
        </section>
    </main>

    <script>
        const years = {json.dumps(years)};
        let capitalData = {json.dumps(capital_curve)};
        let confidenceData = {json.dumps(confidence_curve)};

        const ctxCap = document.getElementById('capitalChart').getContext('2d');
        const chartCap = new Chart(ctxCap, {{
            type: 'line',
            data: {{
                labels: years,
                datasets: [{{
                    label: '{label_cap}',
                    data: capitalData,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: true,
                    tension: 0.3
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});

        const ctxConf = document.getElementById('confidenceChart').getContext('2d');
        const chartConf = new Chart(ctxConf, {{
            type: 'line',
            data: {{
                labels: years,
                datasets: [{{
                    label: '{label_conf}',
                    data: confidenceData,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    fill: true,
                    tension: 0.3
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});

        function updateYearView(val) {{
            const isZh = { 'true' if is_zh else 'false' };
            const yr = years[val];
            document.getElementById('current-year-label').innerText = isZh ? `当前播放年份: ${{yr}}` : `Current Year: ${{yr}}`;
        }}

        function playTimelineAnimation() {{
            let idx = 0;
            const timer = setInterval(() => {{
                document.getElementById('timelineSlider').value = idx;
                updateYearView(idx);
                idx++;
                if (idx >= years.length) clearInterval(timer);
            }}, 800);
        }}

        function injectMacroShock() {{
            capitalData = capitalData.map(v => v * 0.85);
            confidenceData = confidenceData.map(v => Math.max(30, v - 15));
            chartCap.data.datasets[0].data = capitalData;
            chartConf.data.datasets[0].data = confidenceData;
            chartCap.update();
            chartConf.update();
            alert({ '"⚡ 突发大环境冲击已注入！资金下调 15%，信心下调 15%"' if is_zh else '"⚡ Macro shock injected! Capital -15%, Confidence -15%"' });
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
            "timeline_projection": [
                {"year": 2026, "net_worth_usd": 40000, "confidence_score": 0.95},
                {"year": 2027, "net_worth_usd": 55000, "confidence_score": 0.92},
                {"year": 2028, "net_worth_usd": 78000, "confidence_score": 0.88},
                {"year": 2029, "net_worth_usd": 110000, "confidence_score": 0.85},
                {"year": 2030, "net_worth_usd": 150000, "confidence_score": 0.82}
            ]
        }

    out_file = sys.argv[2] if len(sys.argv) > 2 else "lifetree_deduction_player.html"
    res_path = generate_deduction_player_html(data, out_file, lang="zh")
    print(json.dumps({"status": "SUCCESS", "deduction_player_html_path": os.path.abspath(res_path)}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
