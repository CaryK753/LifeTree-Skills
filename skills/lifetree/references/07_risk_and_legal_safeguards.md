# Risk Control & Legal Compliance Safeguards

## 1. Graph Pollution Defense & Confidence Scoring
All nodes and edges carry a mandatory confidence score:
- **Official Government / Institutional Data (`1.0`)**: Direct statutory text / gazettes / official APIs. Rendered as **SOLID lines**.
- **Community Verified Data (`0.8`)**: Crowd-sourced / empirical data. Rendered as **SOLID lines**.
- **Model Prediction Data (`0.5`)**: Predictive LLM projections. Rendered as **DASHED lines**.

## 2. Precise Poison Node Pruning
If a connector plugin is found compromised or producing false information, the system invokes `scripts/graph_confidence_filter.py` with the revoked `Source_ID`, extracting the compromised sub-tree without corrupting the broader knowledge graph.

## 3. Compliance & Professional Advisor Disclaimer Framing
- **Official Source Anchors**: Every node in the UI mandates a click-through hyperlink to the original official statute text or official data source.
- **"Brief for Professional Advisor" Framing**: Exported reports are explicitly formatted as a "Brief for Advisor" (using `resources/brief_for_advisor_template.md`). This ensures final legal, financial, or medical verification is handled by licensed professionals, eliminating platform vicarious liability.
