#!/usr/bin/env python3
"""
LifeTree Vis.js Dynamic Knowledge Graph Viewer Generator (i18n Enhanced)
Generates an interactive force-directed Vis.js network graph viewer featuring dark theme,
node search bar, entity legend, node detail inspector, and full i18n support.
"""

import os
import sys
import json
from typing import Dict, Any, List

def generate_graph_visualizer_html(graph_payload: Dict[str, Any], output_path: str, lang: str = "zh") -> str:
    """
    Generates a single self-contained Vis.js HTML Knowledge Graph Viewer with i18n support.
    """
    nodes_raw = graph_payload.get("nodes", [])
    edges_raw = graph_payload.get("edges", [])
    is_zh = (lang == "zh")

    vis_nodes = []
    for n in nodes_raw:
        nid = n.get("id")
        label = n.get("label", nid)
        etype = n.get("entity_type", "CONCEPT").upper()

        color_map = {
            "PERSON": "#10b981",
            "CAPITAL_ASSET": "#f59e0b",
            "REGULATION_LAW": "#6366f1",
            "PATHWAY_ROUTE": "#ec4899",
            "INSTITUTION_AGENCY": "#8b5cf6",
            "ACTION": "#06b6d4"
        }
        node_color = color_map.get(etype, "#64748b")

        vis_nodes.append({
            "id": nid,
            "label": label,
            "group": etype,
            "color": node_color,
            "shape": "dot",
            "size": 18,
            "raw_data": n
        })

    vis_edges = []
    for e in edges_raw:
        vis_edges.append({
            "from": e.get("source"),
            "to": e.get("target"),
            "label": e.get("relation_type", "IMPACTS"),
            "font": {"color": "#94a3b8", "size": 10},
            "color": {"color": "rgba(255, 255, 255, 0.15)", "highlight": "#34d399"},
            "arrows": {"to": {"enabled": True, "scaleFactor": 0.6}}
        })

    title_text = "LifeTree 知识土壤拓扑查看器" if is_zh else "LifeTree Knowledge Soil Graph Viewer"
    subtitle_text = "力导向图谱 · 实体检索 · 细节下钻" if is_zh else "Force-Directed Graph · Entity Search · Detail Drill-Down"
    search_placeholder = "搜索节点..." if is_zh else "Search node..."
    inspector_title = "🔍 节点属性详情" if is_zh else "🔍 Node Inspector"

    html_content = f"""<!DOCTYPE html>
<html lang="{ 'zh-CN' if is_zh else 'en' }" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LifeTree — {title_text}</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #f8fafc; margin: 0; overflow: hidden; }}
        #graph-container {{ width: 100vw; height: 100vh; background: radial-gradient(circle at 50% 50%, #1e293b 0%, #0b0f19 100%); }}
        .glass-panel {{ background: rgba(17, 24, 39, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.1); }}
        .gradient-text {{ background: linear-gradient(135deg, #34d399 0%, #10b981 50%, #059669 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="absolute top-4 left-4 right-4 z-10 flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl glass-panel shadow-2xl">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-xl">
                🕸️
            </div>
            <div>
                <h1 class="text-lg font-bold text-white tracking-tight">LifeTree <span class="gradient-text">{ '知识图谱查看器' if is_zh else 'Knowledge Graph Viewer' }</span></h1>
                <p class="text-xs text-slate-400">{subtitle_text}</p>
            </div>
        </div>

        <div class="flex items-center gap-3">
            <input type="text" id="searchInput" oninput="searchNode(this.value)" placeholder="{search_placeholder}" class="px-4 py-2 bg-slate-900/80 border border-slate-700 text-white rounded-xl text-xs focus:outline-none focus:border-emerald-500 w-48" />
            <button onclick="resetGraph()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs rounded-xl border border-slate-700">
                { '居中复位' if is_zh else 'Fit Network' }
            </button>
        </div>
    </div>

    <!-- Canvas -->
    <div id="graph-container"></div>

    <!-- Inspector -->
    <div id="inspector" class="absolute top-24 right-4 w-80 z-10 glass-panel rounded-2xl p-5 shadow-2xl hidden border border-slate-700/60">
        <div class="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
                <span>{inspector_title}</span>
            </h3>
            <button onclick="closeInspector()" class="text-slate-400 hover:text-white">&times;</button>
        </div>
        <div id="inspector-body" class="text-xs space-y-2"></div>
    </div>

    <script>
        const nodesData = {json.dumps(vis_nodes, ensure_ascii=False)};
        const edgesData = {json.dumps(vis_edges, ensure_ascii=False)};

        const visNodes = new vis.DataSet(nodesData);
        const visEdges = new vis.DataSet(edgesData);

        const container = document.getElementById('graph-container');
        const data = {{ nodes: visNodes, edges: visEdges }};

        const options = {{
            nodes: {{
                font: {{ color: '#f8fafc', size: 12, face: 'Inter, system-ui, sans-serif' }},
                borderWidth: 2,
                shadow: true
            }},
            physics: {{
                barnesHut: {{ gravitationalConstant: -3000, springLength: 120 }}
            }}
        }};

        const network = new vis.Network(container, data, options);

        network.on("click", function(params) {{
            if (params.nodes.length > 0) {{
                const nid = params.nodes[0];
                const nodeItem = nodesData.find(n => n.id === nid);
                if (nodeItem) openInspector(nodeItem);
            }} else {{
                closeInspector();
            }}
        }});

        function openInspector(nodeItem) {{
            const panel = document.getElementById('inspector');
            const body = document.getElementById('inspector-body');

            const isZh = { 'true' if is_zh else 'false' };
            const n = nodeItem.raw_data || {{}};

            body.innerHTML = `
                <div class="p-3 bg-slate-900/80 rounded-xl border border-slate-800 space-y-2">
                    <div class="font-bold text-emerald-400 text-sm">${{nodeItem.label}}</div>
                    <div class="text-slate-400">ID: <span class="text-slate-200 font-mono">${{nodeItem.id}}</span></div>
                    <div class="text-slate-400">${{isZh ? '实体类型' : 'Type'}}: <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">${{nodeItem.group}}</span></div>
                    <div class="text-slate-400">${{isZh ? '可信度' : 'Confidence'}}: <span class="text-white font-mono">${{n.confidence || 1.0}}</span></div>
                </div>
            `;
            panel.classList.remove('hidden');
        }}

        function closeInspector() {{
            document.getElementById('inspector').classList.add('hidden');
        }}

        function searchNode(val) {{
            if (!val.trim()) return;
            const match = nodesData.find(n => n.label.toLowerCase().includes(val.toLowerCase()));
            if (match) {{
                network.focus(match.id, {{ scale: 1.2, animation: {{ duration: 500 }} }});
                network.selectNodes([match.id]);
                openInspector(match);
            }}
        }}

        function resetGraph() {{
            network.fit({{ animation: {{ duration: 600 }} }});
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
            "nodes": [
                {"id": "usr_person", "label": "Person (Applicant)", "entity_type": "PERSON", "confidence": 1.0},
                {"id": "asset_sperrkonto", "label": "€12,000 Blocked Account", "entity_type": "CAPITAL_ASSET", "confidence": 1.0},
                {"id": "route_bluecard", "label": "EU Blue Card Permit", "entity_type": "PATHWAY_ROUTE", "confidence": 1.0}
            ],
            "edges": [
                {"source": "usr_person", "target": "asset_sperrkonto", "relation_type": "REQUIRES_CAPITAL"},
                {"source": "asset_sperrkonto", "target": "route_bluecard", "relation_type": "CONVERTS_TO"}
            ]
        }

    out_file = sys.argv[2] if len(sys.argv) > 2 else "lifetree_graph_viewer.html"
    res_path = generate_graph_visualizer_html(data, out_file, lang="zh")
    print(json.dumps({"status": "SUCCESS", "graph_visualizer_html_path": os.path.abspath(res_path)}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
