# Interactive HTML Decision Dashboards & Knowledge Graph Viewers

## 1. Rationale: Why Rich Interactive HTML Outputs?
Static Markdown text reports cannot present interactive Vis.js force-directed knowledge graphs, Chart.js probability gauges, or interactive To-Do checkboxes.

LifeTree provides automated generation of single-file self-contained **HTML Decision Dashboards** and **Interactive Knowledge Graph Viewers**:

---

## 2. Interactive Knowledge Graph Viewer (`scripts/graph_engines/graph_visualizer_html.py`)
- **Vis.js Force-Directed Physics Network**: Real-time node dragging, physics simulation, zoom, and panning.
- **Color-Coded Entity Types**: Distinct color badges for `PERSON` (Cyan), `REGULATION_LAW` (Purple), `PATHWAY_ROUTE` (Green), `CAPITAL_ASSET` (Gold), `INSTITUTION_AGENCY` (Blue), `MACRO_EVENT` (Red).
- **Line Confidence Styling**: High-confidence links render as solid lines, low-confidence links ($C < 0.6$) render as dashed lines.
- **Node Inspector Sidebar**: Clicking any node opens a slide-over panel displaying properties, confidence, and source provenance.
- **Fuzzy Search & Filter Controls**: Filter by entity type or search node labels in real-time.

---

## 3. Interactive HTML Decision Dashboard (`scripts/ui_translators/html_report_generator.py`)
- **Executive Metric Cards**: Displays target P50 timeline, 95% VaR budget, execution difficulty, and Regret Minimization score.
- **Actionable Weekly To-Do Checklist**: Includes interactive checkboxes for user task tracking.
- **Chart.js Probability Distribution**: Renders interactive Monte Carlo timeline confidence gauges.
- **Glassmorphism Design**: Dark mode glassmorphism styling with modern typography.
