# Temporal GraphRAG & Knowledge Graph Engine

## 1. Temporal Attributes (`Valid_Time`)
To prevent outdated statutes or obsolete policies from corrupting current decision logic, every node and edge in the LifeTree GraphRAG contains strict temporal scope attributes:
- `Valid_Time.start_time`: ISO 8601 timestamp when the law, policy, or quota became effective (e.g. `2024-06-01T00:00:00Z` for 2024 Chancenkarte launch).
- `Valid_Time.end_time`: Expiration timestamp or `null` if currently active.

Queries automatically filter nodes based on evaluation date:
$$\text{Active}(N) = (T_{\text{eval}} \ge N.\text{Valid\_Time.start\_time}) \land (N.\text{Valid\_Time.end\_time} == \text{null} \lor T_{\text{eval}} \le N.\text{Valid\_Time.end\_time})$$

## 2. Lineage & Provenance (`Source_ID`)
Every ingested item receives a unique `Source_ID` tag tracking its data source plugin or official gazette URL (e.g., `SRC_GOV_DE_BAMF`).

## 3. Core Ontology & Normalization
To prevent graph pollution, all connector payloads are forced through a Core Ontology mapping layer:
- **Node Types**: `POLICY_LAW`, `FEES_REQUIREMENT`, `IMMIGRATION_ROUTE`, `CAREER_ROLE`, `TIMELINE_EVENT`, `RISK_NODE`, `WHAT_IF_HYPOTHESIS`.
- **Edge Relations**: `REQUIRES`, `PREREQUISITE_FOR`, `IMPACTS`, `RISK_OF`, `CONVERTS_TO`, `CONFLICTS_WITH`.

## 4. Poison Tree Cutting (Abnormal Node Pruning)
If a community connector plugin is compromised, revoked, or found to produce false information, the system performs targeted **Poison Tree Cutting** without invalidating the whole graph:
1. Revoke the specific `Source_ID` in the blacklist.
2. Run `scripts/graph_confidence_filter.py` to surgically extract and discard all nodes and edges carrying that `Source_ID`.
3. Re-evaluate connected decision branches; if a branch loses mandatory prerequisites, mark it as a `DEAD_BRANCH`.
