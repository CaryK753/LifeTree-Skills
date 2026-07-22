import json
import os
import sys
from typing import Dict, Any

def generate_graph_visualizer_html(graph_payload: Dict[str, Any], output_path: str, lang: str = "zh") -> str:
    """
    Generates a standalone HTML file containing a Vis.js force-directed graph visualization
    with a clean, dark SaaS-style design.
    """
    nodes_data = json.dumps(graph_payload.get('nodes', []))
    edges_data = json.dumps(graph_payload.get('edges', []))

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>知识图谱 (Knowledge Graph)</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <!-- Vis.js Network -->
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Inter', 'sans-serif'],
                    }},
                    colors: {{
                        base: '#0c0c14',
                        surface: '#16161f',
                        surfaceHover: '#1e1e2a',
                        borderBase: '#2a2a3a',
                        textBase: '#e8e8ee',
                        textMuted: '#8888a0',
                        entityPERSON: '#22c55e',
                        entityASSET: '#f59e0b',
                        entityLAW: '#6366f1',
                        entityPATH: '#ec4899',
                        entityINST: '#8b5cf6',
                        entityACTION: '#06b6d4'
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{
            background-color: #0c0c14;
            color: #e8e8ee;
            font-family: 'Inter', sans-serif;
            margin: 0;
            overflow: hidden; /* Prevent body scroll */
        }}
        #mynetwork {{
            width: 100%;
            height: calc(100vh - 64px); /* Full height minus header */
            outline: none;
        }}
        .vis-network:focus {{
            outline: none;
        }}
        /* Custom scrollbar for inspector */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: #16161f; 
        }}
        ::-webkit-scrollbar-thumb {{
            background: #2a2a3a; 
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #8888a0; 
        }}
    </style>
</head>
<body class="flex flex-col h-screen text-textBase bg-base">

    <!-- Header -->
    <header class="h-16 flex items-center justify-between px-6 border-b border-borderBase bg-surface z-10 shrink-0">
        <div class="flex items-center gap-4">
            <div class="flex items-center gap-2 text-textBase font-semibold text-lg">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-entityLAW"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                知识图谱
            </div>
            <span class="text-borderBase">|</span>
            <a href="/" class="text-sm text-textMuted hover:text-textBase transition-colors">返回首页</a>
        </div>
        
        <div class="flex items-center gap-3">
            <div class="relative">
                <input type="text" id="searchInput" placeholder="搜索节点..." 
                    class="bg-base border border-borderBase rounded-lg py-1.5 pl-3 pr-8 text-sm focus:outline-none focus:border-textMuted placeholder-textMuted transition-colors w-64 text-textBase">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute right-2.5 top-2 text-textMuted pointer-events-none"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            </div>
            <button id="resetBtn" class="px-3 py-1.5 text-sm font-medium border border-borderBase rounded-lg hover:bg-surfaceHover hover:border-textMuted transition-colors text-textMuted hover:text-textBase">
                重置视图
            </button>
        </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 relative flex w-full h-full overflow-hidden">
        
        <!-- Graph Container -->
        <div id="mynetwork" class="flex-1 w-full h-full"></div>

        <!-- Legend -->
        <div class="absolute bottom-6 left-6 bg-surface border border-borderBase rounded-xl p-4 shadow-lg pointer-events-auto">
            <h3 class="text-xs font-semibold text-textMuted uppercase tracking-wider mb-3">实体类型</h3>
            <div class="flex flex-col gap-2">
                <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-entityPERSON"></div><span class="text-sm">个人 (PERSON)</span></div>
                <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-entityASSET"></div><span class="text-sm">资产 (CAPITAL_ASSET)</span></div>
                <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-entityLAW"></div><span class="text-sm">法规 (REGULATION_LAW)</span></div>
                <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-entityPATH"></div><span class="text-sm">路径 (PATHWAY_ROUTE)</span></div>
                <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-entityINST"></div><span class="text-sm">机构 (INSTITUTION_AGENCY)</span></div>
                <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-entityACTION"></div><span class="text-sm">行为 (ACTION)</span></div>
            </div>
        </div>

        <!-- Inspector Panel -->
        <aside id="inspector" class="w-80 bg-surface border-l border-borderBase flex flex-col h-full transform transition-transform duration-300 translate-x-full absolute right-0 top-0 bottom-0 z-20">
            <div class="p-4 border-b border-borderBase flex items-center justify-between shrink-0">
                <h2 class="text-base font-semibold">详细信息</h2>
                <button id="closeInspectorBtn" class="p-1 rounded hover:bg-surfaceHover text-textMuted hover:text-textBase transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                </button>
            </div>
            <div id="inspectorContent" class="p-4 overflow-y-auto flex-1 text-sm text-textMuted">
                请在图谱中点击一个节点查看详情。
            </div>
        </aside>
    </main>

    <script>
        const colorMap = {{
            'PERSON': '#22c55e',
            'CAPITAL_ASSET': '#f59e0b',
            'REGULATION_LAW': '#6366f1',
            'PATHWAY_ROUTE': '#ec4899',
            'INSTITUTION_AGENCY': '#8b5cf6',
            'ACTION': '#06b6d4'
        }};

        const rawNodes = {nodes_data};
        const rawEdges = {edges_data};

        // Format nodes for Vis.js
        const nodesData = rawNodes.map(n => ({{
            id: n.id,
            label: n.label || n.id,
            group: n.entity_type,
            title: n.id, // Tooltip
            color: {{
                background: '#16161f',
                border: colorMap[n.entity_type] || '#8888a0',
                highlight: {{
                    background: colorMap[n.entity_type] || '#8888a0',
                    border: '#e8e8ee'
                }}
            }},
            font: {{ color: '#e8e8ee', face: 'Inter' }},
            shape: 'dot',
            size: n.confidence ? 10 + (n.confidence * 10) : 15,
            borderWidth: 2,
            _rawData: n // Store original data for inspector
        }}));

        // Format edges
        const edgesData = rawEdges.map(e => ({{
            from: e.source,
            to: e.target,
            label: e.relation_type,
            font: {{ color: '#8888a0', face: 'Inter', size: 10, align: 'middle', background: '#0c0c14' }},
            color: {{ color: '#2a2a3a', highlight: '#8888a0' }},
            arrows: 'to',
            width: e.confidence ? e.confidence * 2 : 1
        }}));

        const container = document.getElementById('mynetwork');
        const data = {{
            nodes: new vis.DataSet(nodesData),
            edges: new vis.DataSet(edgesData)
        }};
        const options = {{
            nodes: {{
                shapeProperties: {{ interpolation: false }}
            }},
            physics: {{
                barnesHut: {{
                    gravitationalConstant: -2000,
                    centralGravity: 0.1,
                    springLength: 150,
                    springConstant: 0.04,
                    damping: 0.09
                }},
                stabilization: {{ iterations: 150 }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200,
                hideEdgesOnDrag: true
            }}
        }};

        const network = new vis.Network(container, data, options);

        // UI Interactions
        const inspector = document.getElementById('inspector');
        const inspectorContent = document.getElementById('inspectorContent');
        const searchInput = document.getElementById('searchInput');

        function openInspector(nodeId) {{
            const node = nodesData.find(n => n.id === nodeId);
            if (!node) return;
            
            const raw = node._rawData;
            const typeColor = colorMap[raw.entity_type] || '#8888a0';
            
            let html = `
                <div class="mb-6">
                    <div class="inline-flex items-center px-2 py-1 rounded text-xs font-medium mb-3 border" style="color: ${{typeColor}}; border-color: ${{typeColor}}33; background-color: ${{typeColor}}11;">
                        ${{raw.entity_type || 'UNKNOWN'}}
                    </div>
                    <h3 class="text-lg font-semibold text-textBase break-words">${{raw.label || raw.id}}</h3>
                    <p class="mt-1 text-xs text-textMuted">ID: ${{raw.id}}</p>
                </div>
            `;

            if (raw.confidence !== undefined) {{
                html += `
                <div class="mb-4">
                    <div class="text-xs font-semibold text-textBase mb-1">置信度 (Confidence)</div>
                    <div class="w-full bg-base rounded-full h-1.5 mt-2 border border-borderBase">
                        <div class="h-1.5 rounded-full" style="width: ${{raw.confidence * 100}}%; background-color: ${{typeColor}}"></div>
                    </div>
                    <div class="text-right text-xs mt-1">${{(raw.confidence * 100).toFixed(0)}}%</div>
                </div>`;
            }}

            if (raw.properties && Object.keys(raw.properties).length > 0) {{
                html += `<div class="mt-6"><h4 class="text-xs font-semibold text-textBase mb-2 border-b border-borderBase pb-1">属性 (Properties)</h4><div class="space-y-2 mt-3">`;
                for (const [k, v] of Object.entries(raw.properties)) {{
                    html += `
                    <div class="flex flex-col gap-0.5">
                        <span class="text-xs font-medium text-textBase">${{k}}</span>
                        <span class="text-sm bg-base p-2 rounded border border-borderBase break-words">${{v}}</span>
                    </div>`;
                }}
                html += `</div></div>`;
            }}
            
            inspectorContent.innerHTML = html;
            inspector.classList.remove('translate-x-full');
            inspector.style.position = 'relative';
        }}

        function closeInspector() {{
            inspector.classList.add('translate-x-full');
            inspector.style.position = 'absolute';
            network.unselectAll();
        }}

        network.on("click", function (params) {{
            if (params.nodes.length > 0) {{
                openInspector(params.nodes[0]);
            }} else {{
                closeInspector();
            }}
        }});

        document.getElementById('closeInspectorBtn').addEventListener('click', closeInspector);
        
        document.getElementById('resetBtn').addEventListener('click', () => {{
            network.fit({{ animation: {{ duration: 500, easingFunction: 'easeInOutQuad' }} }});
            closeInspector();
            searchInput.value = '';
        }});

        // Basic Search functionality
        searchInput.addEventListener('input', (e) => {{
            const val = e.target.value.toLowerCase();
            if (!val) {{
                network.unselectAll();
                return;
            }}
            
            const matchedNodes = nodesData.filter(n => (n.label && n.label.toLowerCase().includes(val)) || (n.id && n.id.toLowerCase().includes(val))).map(n => n.id);
            if (matchedNodes.length > 0) {{
                network.selectNodes(matchedNodes);
                if(matchedNodes.length === 1) openInspector(matchedNodes[0]);
            }} else {{
                network.unselectAll();
            }}
        }});

    </script>
</body>
</html>"""

    # Write to file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    except (OSError, IOError) as e:
        print(f"Warning: failed to write graph visualizer HTML to {output_path}: {e}", file=sys.stderr)
        return None

    return output_path


def main():
    # Example demo data
    demo_payload = {
        "nodes": [
            {"id": "n1", "label": "张三", "entity_type": "PERSON", "confidence": 0.95, "properties": {"age": 45, "role": "CEO"}},
            {"id": "n2", "label": "李四", "entity_type": "PERSON", "confidence": 0.8},
            {"id": "n3", "label": "王五集团", "entity_type": "INSTITUTION_AGENCY", "confidence": 0.9, "properties": {"industry": "Finance"}},
            {"id": "n4", "label": "境外账户A", "entity_type": "CAPITAL_ASSET", "confidence": 0.7},
            {"id": "n5", "label": "反洗钱法2024", "entity_type": "REGULATION_LAW", "confidence": 1.0},
            {"id": "n6", "label": "资金转移路径B", "entity_type": "PATHWAY_ROUTE", "confidence": 0.85},
            {"id": "n7", "label": "高频交易", "entity_type": "ACTION", "confidence": 0.9}
        ],
        "edges": [
            {"source": "n1", "target": "n3", "relation_type": "FOUNDER", "confidence": 0.9},
            {"source": "n3", "target": "n4", "relation_type": "OWNS", "confidence": 0.8},
            {"source": "n1", "target": "n2", "relation_type": "ASSOCIATE", "confidence": 0.7},
            {"source": "n2", "target": "n7", "relation_type": "PERFORMS", "confidence": 0.85},
            {"source": "n7", "target": "n6", "relation_type": "CREATES", "confidence": 0.9},
            {"source": "n6", "target": "n5", "relation_type": "VIOLATES", "confidence": 0.6}
        ]
    }
    
    output_html = "demo_graph.html"
    generate_graph_visualizer_html(demo_payload, output_html)
    print(f"Generated demo HTML at {output_html}")

if __name__ == "__main__":
    main()
