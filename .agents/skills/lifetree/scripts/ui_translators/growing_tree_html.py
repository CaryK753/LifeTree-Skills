#!/usr/bin/env python3
"""
LifeTree Growing Decision Tree HTML Viewer Generator
Generates a self-contained HTML file featuring a responsive, animated "Growing Tree" visualization.
Branches represent future choice trajectories, fruits represent PR/Citizenship goals,
side buds represent Plan B hedges, and withered branches represent pruned high-risk paths.
"""

import os
import sys
import json
from typing import Dict, Any, List

def generate_growing_tree_html(deduction_data: Dict[str, Any], output_path: str) -> str:
    """
    Generates a single self-contained HTML file displaying an interactive growing decision tree.
    """
    summary = deduction_data.get("deduction_summary", {})
    traj_a = deduction_data.get("pathway_a_trajectory", [])
    traj_b = deduction_data.get("pathway_b_trajectory", [])

    # Construct Tree Node Hierarchy
    nodes = [
        {"id": "root_soil", "label": "🌱 Knowledge Soil\n(Statutory Laws & Constraints)", "group": "SOIL", "level": 0, "color": "#78350f"},
        {"id": "trunk_user", "label": "🪵 Current State (Year 0)\n(31 Yo, MS CS, $40k, A2 German)", "group": "TRUNK", "level": 1, "color": "#059669"}
    ]
    edges = [
        {"from": "root_soil", "to": "trunk_user", "label": "Nourishes"}
    ]

    # Branch A Nodes (Chancenkarte -> Blue Card)
    prev_id = "trunk_user"
    for step in traj_a:
        yr = step["year"]
        nid = f"branch_a_y{yr}"
        prob_pct = int(step["success_probability"] * 100)
        badge = step.get("badge", "")

        is_fruit = prob_pct >= 95
        is_plan_b = step.get("plan_b_active", False)

        shape_type = "star" if is_fruit else ("diamond" if is_plan_b else "dot")
        node_color = "#34d399" if is_fruit else ("#fbbf24" if is_plan_b else "#10b981")
        node_label = f"🌿 Y{yr}: Pathway A ({prob_pct}%)\n${step['capital_balance_usd']:,.0f}"
        if is_fruit:
            node_label = f"🏆 Y{yr}: PR Unlocked!\n({prob_pct}% Success)"

        nodes.append({
            "id": nid,
            "label": node_label,
            "group": "BRANCH_A",
            "level": yr + 1,
            "color": node_color,
            "shape": shape_type,
            "raw_data": step
        })
        edges.append({"from": prev_id, "to": nid, "label": f"Year {yr}"})
        prev_id = nid

        # Add Side Bud (Plan B) if active
        if is_plan_b:
            bud_id = f"side_bud_y{yr}"
            nodes.append({
                "id": bud_id,
                "label": f"🛡️ Plan B Side Bud (Y{yr})\n(Remote Freelance Hedge)",
                "group": "SIDE_BUD",
                "level": yr + 1,
                "color": "#f59e0b",
                "shape": "triangle"
            })
            edges.append({"from": nid, "to": bud_id, "label": "Sprouts Plan B", "dashes": True})

    # Branch B Nodes (Direct Employer)
    prev_id = "trunk_user"
    for step in traj_b:
        yr = step["year"]
        nid = f"branch_b_y{yr}"
        prob_pct = int(step["success_probability"] * 100)

        is_fruit = prob_pct >= 95
        node_color = "#60a5fa" if not is_fruit else "#6366f1"
        node_label = f"🌿 Y{yr}: Pathway B ({prob_pct}%)\n${step['capital_balance_usd']:,.0f}"
        if is_fruit:
            node_label = f"🏆 Y{yr}: Pathway B PR!\n({prob_pct}% Success)"

        nodes.append({
            "id": nid,
            "label": node_label,
            "group": "BRANCH_B",
            "level": yr + 1,
            "color": node_color,
            "shape": "star" if is_fruit else "dot",
            "raw_data": step
        })
        edges.append({"from": prev_id, "to": nid, "label": f"Year {yr}"})
        prev_id = nid

    # Add Dead Branch (Withered High Risk Path)
    nodes.append({
        "id": "dead_branch_01",
        "label": "🥀 Pruned High-Friction Path\n(Blocked Student Visa)",
        "group": "DEAD_BRANCH",
        "level": 2,
        "color": "#ef4444",
        "shape": "cross"
    })
    edges.append({"from": "trunk_user", "to": "dead_branch_01", "label": "Pruned", "dashes": True, "color": "#ef4444"})

    html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LifeTree — Growing Decision Tree Visualizer</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #f8fafc; margin: 0; overflow: hidden; }}
        #tree-container {{ width: 100vw; height: 100vh; background: radial-gradient(circle at 50% 90%, #1e293b 0%, #0b0f19 100%); }}
        .glass-panel {{ background: rgba(17, 24, 39, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.1); }}
        .gradient-text {{ background: linear-gradient(135deg, #34d399 0%, #10b981 50%, #059669 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    </style>
</head>
<body>
    <!-- Top Control Bar -->
    <div class="absolute top-4 left-4 right-4 z-10 flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl glass-panel shadow-2xl">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-xl">
                🌳
            </div>
            <div>
                <h1 class="text-lg font-bold text-white tracking-tight">LifeTree <span class="gradient-text">Growing Decision Tree</span></h1>
                <p class="text-xs text-slate-400">Future Choice Branching & Temporal Trajectory Visualizer</p>
            </div>
        </div>

        <!-- Controls -->
        <div class="flex items-center gap-3">
            <button onclick="playGrowthAnimation()" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm rounded-xl transition-all shadow-lg shadow-emerald-900/30 flex items-center gap-2">
                <span>▶ Play Tree Growth</span>
            </button>
            <button onclick="resetTreeLayout()" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-white font-semibold text-sm rounded-xl transition-all border border-slate-700">
                Fit Layout
            </button>
        </div>
    </div>

    <!-- Tree Canvas -->
    <div id="tree-container"></div>

    <!-- Inspector Drawer -->
    <div id="node-inspector" class="absolute top-24 right-4 bottom-4 w-96 z-10 glass-panel rounded-2xl p-6 shadow-2xl overflow-y-auto hidden border border-slate-700/60">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
            <h2 class="text-base font-bold text-white flex items-center gap-2">
                <span>🍃 Branch Inspector</span>
            </h2>
            <button onclick="closeInspector()" class="text-slate-400 hover:text-white text-lg">&times;</button>
        </div>
        <div id="inspector-content"></div>
    </div>

    <script>
        const rawNodes = {json.dumps(nodes, ensure_ascii=False)};
        const rawEdges = {json.dumps(edges, ensure_ascii=False)};

        const visNodes = new vis.DataSet();
        const visEdges = new vis.DataSet();

        const container = document.getElementById('tree-container');
        const data = {{ nodes: visNodes, edges: visEdges }};

        const options = {{
            layout: {{
                hierarchical: {{
                    direction: 'BU', // Bottom to Up (Tree grows upward)
                    sortMethod: 'directed',
                    nodeSpacing: 180,
                    levelSeparation: 130
                }}
            }},
            nodes: {{
                font: {{ color: '#f8fafc', size: 13, face: 'Inter, system-ui, sans-serif' }},
                borderWidth: 2,
                shadow: true
            }},
            edges: {{
                color: {{ color: 'rgba(16, 185, 129, 0.5)', highlight: '#34d399' }},
                arrows: {{ to: {{ enabled: true, scaleFactor: 0.8 }} }},
                smooth: {{ type: 'cubicBezier', forceDirection: 'vertical', roundness: 0.4 }}
            }},
            physics: {{ hierarchicalRepulsion: {{ nodeDistance: 160 }} }}
        }};

        const network = new vis.Network(container, data, options);

        network.on("click", function(params) {{
            if (params.nodes.length > 0) {{
                const nid = params.nodes[0];
                const nodeItem = rawNodes.find(n => n.id === nid);
                if (nodeItem) openInspector(nodeItem);
            }} else {{
                closeInspector();
            }}
        }});

        function playGrowthAnimation() {{
            visNodes.clear();
            visEdges.clear();

            // Sort nodes by level
            const levels = [0, 1, 2, 3, 4, 5, 6];
            let delay = 0;

            levels.forEach(lvl => {{
                setTimeout(() => {{
                    const lvlNodes = rawNodes.filter(n => n.level === lvl);
                    lvlNodes.forEach(n => visNodes.add(n));

                    const lvlNodeIds = new Set(lvlNodes.map(n => n.id));
                    const lvlEdges = rawEdges.filter(e => lvlNodeIds.has(e.to));
                    lvlEdges.forEach(e => visEdges.add(e));
                }}, delay);
                delay += 700;
            }});
        }}

        function openInspector(nodeData) {{
            const panel = document.getElementById('node-inspector');
            const content = document.getElementById('inspector-content');

            let detailsHtml = '';
            if (nodeData.raw_data) {{
                const d = nodeData.raw_data;
                detailsHtml = `
                    <div class="space-y-3 bg-slate-900/60 p-4 rounded-xl border border-slate-800 text-xs">
                        <div class="flex justify-between"><span class="text-slate-400">Success Probability:</span><span class="text-emerald-400 font-bold font-mono">${{(d.success_probability * 100).toFixed(0)}}%</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">Capital Balance:</span><span class="text-white font-mono">$${{d.capital_balance_usd.toLocaleString()}}</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">Trajectory Badge:</span><span class="text-amber-300 font-semibold">${{d.badge || 'NORMAL'}}</span></div>
                    </div>
                `;
            }}

            content.innerHTML = `
                <div class="space-y-4">
                    <div>
                        <span class="px-2.5 py-1 text-xs font-bold rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                            ${{nodeData.group}}
                        </span>
                        <h3 class="text-base font-bold text-white mt-2">${{nodeData.label.replace('\\n', ' — ')}}</h3>
                    </div>
                    ${{detailsHtml}}
                </div>
            `;
            panel.classList.remove('hidden');
        }}

        function closeInspector() {{
            document.getElementById('node-inspector').classList.add('hidden');
        }}

        function resetTreeLayout() {{
            network.fit({{ animation: {{ duration: 800, easingFunction: 'easeInOutQuad' }} }});
        }}

        // Auto-play growth on load
        playGrowthAnimation();
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
            "deduction_summary": {"timeline_horizon_years": 5},
            "pathway_a_trajectory": [
                {"year": 1, "success_probability": 0.85, "capital_balance_usd": 26000.0, "badge": "OPTIMAL_PROGRESSION"},
                {"year": 2, "success_probability": 0.90, "capital_balance_usd": 46000.0, "badge": "OPTIMAL_PROGRESSION", "plan_b_active": True},
                {"year": 3, "success_probability": 0.98, "capital_balance_usd": 76000.0, "badge": "PR_ELIGIBLE"}
            ],
            "pathway_b_trajectory": [
                {"year": 1, "success_probability": 0.70, "capital_balance_usd": 35000.0, "badge": "HIGH_FRICTION_PROGRESSION"},
                {"year": 2, "success_probability": 0.65, "capital_balance_usd": 60000.0, "badge": "HIGH_FRICTION_PROGRESSION"},
                {"year": 3, "success_probability": 0.75, "capital_balance_usd": 95000.0, "badge": "OPTIMAL_PROGRESSION"}
            ]
        }

    out_file = sys.argv[2] if len(sys.argv) > 2 else "lifetree_growing_tree.html"
    res_path = generate_growing_tree_html(data, out_file)
    print(json.dumps({"status": "SUCCESS", "growing_tree_html_path": os.path.abspath(res_path)}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
