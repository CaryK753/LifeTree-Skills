# Object-Centric Temporal Knowledge Graph & GraphRAG Architecture

## 1. Object-Centric Dynamic Ontology
LifeTree models complex personal decisions as an **Object-Centric Dynamic Ontology**:

### Ontology Objects
- `PERSON`: User, spouse, dependents, employer.
- `REGULATION_LAW`: Statutes, immigration acts, tax codes, CPI indexes.
- `PATHWAY_ROUTE`: Residence permits, golden visas, career pivots, study programs.
- `CAPITAL_ASSET`: Liquid cash reserves, real estate, Sperrkonto deposits, stocks.
- `INSTITUTION_AGENCY`: Embassies, tax authorities, universities, central banks.
- `MACRO_EVENT`: Geopolitical conflicts, interest rate hikes, election shifts, quota freezes.
- `ACTION`: State mutations (`ApplyVisa`, `DepositCapital`, `ConvertTaxResidency`).

### Kinetic Links (Edges)
Objects are connected via weighted, directional, temporal **Kinetic Links**:
`DEPENDS_ON`, `GOVERNS`, `REQUIRES_CAPITAL`, `TRIGGERS_EVENT`, `MUTATES_STATE`, `CONFLICTS_WITH`, `DERIVES_FROM`.

Each link carries a Kinetic Weight ($W$), Friction Penalty ($F$), Temporal Scope (`Valid_Time`), Provenance (`Source_ID`), and Confidence Score ($C$).

---

## 2. Code-Driven Graph Algorithms (`scripts/temporal_graph_engine.py`)

> [!IMPORTANT]
> **STRICT CODE-DRIVEN COMPUTATION POLICY**:
> All graph traversal, Dijkstra shortest path finding, multi-hop risk cascades, and bottleneck identification MUST be calculated by executing Python code (`scripts/temporal_graph_engine.py`). The LLM must NEVER manually estimate graph distances or friction costs!

### A. Dijkstra Causal Pathfinding (Lowest-Friction Route)
Computes the optimal path connecting a user `PERSON` object to a target `PATHWAY_ROUTE` object through the ontology network:
$$\text{Cost}(E) = \frac{1.0}{C_E \cdot W_E} + F_E$$
Finds the path minimizing cumulative friction while maximizing link confidence.

### B. Multi-Hop Risk Cascade Propagation
When a macro shock occurs (e.g. rate hike or quota cut on a `MACRO_EVENT` node), the engine propagates risk intensity across $N$-hop Kinetic Links, computing decay and identifying downstream impacted target objects.

### C. Degree & Betweenness Bottleneck Identification
Audits node degree and centrality to highlight **Single Points of Failure** (e.g., a specific language exam or embassy appointment delay) that threaten the decision graph, recommending targeted Plan B hedges.
