#!/usr/bin/env python3
"""
LifeTree Growing Decision Tree HTML Viewer Generator
Generates an interactive Vis.js decision tree visualization with clean SaaS-style design.
"""

import os
import sys
import json
from typing import Dict, Any


def generate_growing_tree_html(deduction_data: Dict[str, Any], output_path: str, lang: str = "zh") -> str:
    """Generates a Vis.js interactive decision tree HTML page."""
    path_a = deduction_data.get("pathway_a_trajectory", [])
    path_b = deduction_data.get("pathway_b_trajectory", [])

    nodes = [{"id": "root", "label": "当前状态\\n决策起点", "level": 0,
              "color": {"background": "#1e1e2a", "border": "#2a2a3a"},
              "font": {"color": "#e8e8ee"}, "shape": "box",
              "data": {"year": 0, "desc": "决策起点"}}]
    edges = []

    prev_id = "root"
    for step in path_a:
        yr = step.get("year", 1)
        prob = step.get("success_probability", 0)
        cap = step.get("capital_balance_usd", 0)
        badge = step.get("badge", "")
        plan_b = step.get("plan_b_active", False)
        nid = f"a_{yr}"
        bg = "#f59e0b" if plan_b else "#22c55e"
        nodes.append({"id": nid, "label": f"第{yr}年 方案A\\n{prob}%", "level": yr,
                       "color": {"background": bg, "border": bg},
                       "font": {"color": "#0c0c14"}, "shape": "box",
                       "data": {"year": yr, "prob": prob, "capital": cap, "badge": badge, "plan_b": plan_b, "path": "A"}})
        edges.append({"from": prev_id, "to": nid, "color": {"color": "#2a2a3a"}})
        prev_id = nid

    prev_id = "root"
    for step in path_b:
        yr = step.get("year", 1)
        prob = step.get("success_probability", 0)
        cap = step.get("capital_balance_usd", 0)
        badge = step.get("badge", "")
        nid = f"b_{yr}"
        nodes.append({"id": nid, "label": f"第{yr}年 方案B\\n{prob}%", "level": yr,
                       "color": {"background": "#6366f1", "border": "#6366f1"},
                       "font": {"color": "#ffffff"}, "shape": "box",
                       "data": {"year": yr, "prob": prob, "capital": cap, "badge": badge, "plan_b": False, "path": "B"}})
        edges.append({"from": prev_id, "to": nid, "color": {"color": "#2a2a3a"}})
        prev_id = nid

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)

    html_template = """<!DOCTYPE html>
<html lang="__LANG__">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LifeTree · 决策树推演</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body { font-family: 'Inter', sans-serif; background: #0c0c14; color: #e8e8ee; margin: 0; overflow: hidden; }
        #network { width: 100vw; height: calc(100vh - 56px); }
        #inspector { transition: transform 0.25s ease; transform: translateX(100%); }
        #inspector.open { transform: translateX(0); }
    </style>
</head>
<body class="flex flex-col h-screen">
    <header class="h-14 bg-[#16161f] border-b border-[#2a2a3a] flex items-center justify-between px-6 shrink-0 z-10">
        <div class="flex items-center gap-4">
            <a href="lifetree_homepage.html" class="text-[#8888a0] hover:text-white text-sm">← 返回首页</a>
            <div class="h-4 w-px bg-[#2a2a3a]"></div>
            <h1 class="text-sm font-semibold">🌳 决策树推演</h1>
        </div>
        <div class="flex items-center gap-2">
            <button id="btn-reset" class="px-3 py-1.5 text-xs font-medium border border-[#2a2a3a] rounded-lg hover:bg-[#1e1e2a]">重置视图</button>
            <button id="btn-play" class="px-3 py-1.5 text-xs font-medium bg-[#6366f1] text-white rounded-lg hover:bg-[#4f46e5]">▶ 播放动画</button>
        </div>
    </header>
    <main class="flex-1 relative">
        <div id="network"></div>
        <aside id="inspector" class="absolute top-0 right-0 h-full w-80 bg-[#16161f] border-l border-[#2a2a3a] z-20 flex flex-col">
            <div class="p-4 border-b border-[#2a2a3a] flex items-center justify-between">
                <h2 class="font-semibold text-sm">节点详情</h2>
                <button id="btn-close" class="text-[#8888a0] hover:text-white text-lg">&times;</button>
            </div>
            <div class="p-4 overflow-y-auto flex-1" id="inspector-content">
                <div class="text-[#8888a0] text-sm text-center mt-10">点击节点查看详情</div>
            </div>
        </aside>
    </main>
    <script>
        const nodesData = __NODES_JSON__;
        const edgesData = __EDGES_JSON__;
        const container = document.getElementById('network');
        let network = null;
        const inspector = document.getElementById('inspector');
        const inspContent = document.getElementById('inspector-content');
        const opts = {
            layout: { hierarchical: { direction: 'DU', sortMethod: 'directed', levelSeparation: 120, nodeSpacing: 200 } },
            nodes: { shape: 'box', margin: 10, borderWidth: 1, shadow: { enabled: true, color: 'rgba(0,0,0,0.3)', size: 8 }, font: { face: 'Inter', size: 13, multi: true } },
            edges: { width: 2, smooth: { type: 'cubicBezier', forceDirection: 'vertical', roundness: 0.4 }, arrows: { to: { enabled: true, scaleFactor: 0.5 } } },
            interaction: { hover: true, zoomView: true, dragView: true },
            physics: false
        };
        function init(animate) {
            const data = { nodes: new vis.DataSet(nodesData), edges: new vis.DataSet(edgesData) };
            network = new vis.Network(container, data, opts);
            network.on("click", function(p) { if (p.nodes.length > 0) showInsp(data.nodes.get(p.nodes[0])); else closeInsp(); });
            if (animate) network.fit({ animation: { duration: 800, easingFunction: 'easeInOutQuad' } });
            else network.fit();
        }
        function fmtMoney(v) { return '$' + v.toLocaleString(); }
        function showInsp(node) {
            inspector.classList.add('open');
            if (!node.data) { inspContent.innerHTML = '<div class="text-[#8888a0] text-sm">无数据</div>'; return; }
            const d = node.data;
            let h = '<div class="text-xs text-[#8888a0] mb-1">节点</div><div class="text-sm font-semibold mb-4">' + node.label.replace('\\n',' ') + '</div>';
            if (d.path) {
                h += '<div class="space-y-0">';
                h += '<div class="flex justify-between text-sm py-2.5 border-t border-[#2a2a3a]"><span class="text-[#8888a0]">路径</span><span class="font-medium">' + (d.path==='A'?'方案 A':'方案 B') + '</span></div>';
                h += '<div class="flex justify-between text-sm py-2.5 border-t border-[#2a2a3a]"><span class="text-[#8888a0]">时间</span><span class="font-medium">第 ' + d.year + ' 年</span></div>';
                h += '<div class="flex justify-between text-sm py-2.5 border-t border-[#2a2a3a]"><span class="text-[#8888a0]">成功率</span><span class="font-medium text-[#22c55e]">' + d.prob + '%</span></div>';
                h += '<div class="flex justify-between text-sm py-2.5 border-t border-[#2a2a3a]"><span class="text-[#8888a0]">资金</span><span class="font-medium">' + fmtMoney(d.capital) + '</span></div>';
                if (d.badge) h += '<div class="flex justify-between text-sm py-2.5 border-t border-[#2a2a3a]"><span class="text-[#8888a0]">标记</span><span class="font-medium">' + d.badge + '</span></div>';
                if (d.plan_b) h += '<div class="mt-3 p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-[#f59e0b]">⚠ Plan B 已激活</div>';
                h += '</div>';
            }
            inspContent.innerHTML = h;
        }
        function closeInsp() { inspector.classList.remove('open'); if (network) network.unselectAll(); }
        init(true);
        document.getElementById('btn-reset').addEventListener('click', () => { network.fit({ animation: { duration: 600 } }); closeInsp(); });
        document.getElementById('btn-play').addEventListener('click', () => {
            closeInsp();
            const d = { nodes: new vis.DataSet([nodesData[0]]), edges: new vis.DataSet([]) };
            network = new vis.Network(container, d, opts);
            network.on("click", function(p) { if (p.nodes.length > 0) showInsp(d.nodes.get(p.nodes[0])); else closeInsp(); });
            let i = 1;
            const iv = setInterval(() => {
                if (i < nodesData.length) {
                    d.nodes.add(nodesData[i]);
                    const e = edgesData.find(e => e.to === nodesData[i].id);
                    if (e) d.edges.add(e);
                    network.fit({ animation: { duration: 400 } });
                    i++;
                } else clearInterval(iv);
            }, 500);
        });
        document.getElementById('btn-close').addEventListener('click', closeInsp);
    </script>
</body>
</html>"""

    html_content = html_template.replace("__LANG__", lang).replace("__NODES_JSON__", nodes_json).replace("__EDGES_JSON__", edges_json)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return output_path


def main():
    data = {
        "pathway_a_trajectory": [
            {"year": 1, "success_probability": 85, "capital_balance_usd": 26000, "badge": "OPTIMAL"},
            {"year": 2, "success_probability": 90, "capital_balance_usd": 46000, "badge": "OPTIMAL", "plan_b_active": True},
            {"year": 3, "success_probability": 98, "capital_balance_usd": 76000, "badge": "PR_ELIGIBLE"}
        ],
        "pathway_b_trajectory": [
            {"year": 1, "success_probability": 70, "capital_balance_usd": 35000, "badge": "HIGH_FRICTION"},
            {"year": 2, "success_probability": 65, "capital_balance_usd": 60000, "badge": "HIGH_FRICTION"},
            {"year": 3, "success_probability": 75, "capital_balance_usd": 95000, "badge": "OPTIMAL"}
        ]
    }
    out_file = sys.argv[1] if len(sys.argv) > 1 else "lifetree_growing_tree.html"
    res_path = generate_growing_tree_html(data, out_file, lang="zh")
    print(json.dumps({"status": "SUCCESS", "path": os.path.abspath(res_path)}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
