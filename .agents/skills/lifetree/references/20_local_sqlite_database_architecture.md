# Embedded Local SQLite Graph Storage & RAG Engine Architecture

## 1. Rationale: Why Embedded Local SQLite Database?
Relying on raw JSON files or in-memory Python dictionaries degrades in performance as knowledge graphs and decision journals expand over years of multi-topic use.

LifeTree adopts **Embedded Local SQLite** (`scripts/sqlite_graph_store.py`):
- **Zero External Dependencies**: Uses Python's standard library `sqlite3` module. Runs 100% locally out-of-the-box on Mac, Linux, and Windows with zero pip/server installation.
- **Hybrid Relational + JSON Storage**: High-performance SQL tables (`ontology_nodes`, `ontology_edges`, `user_memory`, `decision_journal`, `surveillance_registry`) combined with JSON fields.
- **Indexed Graph Traversal**: B-Tree SQL indexes on `source_node`, `target_node`, `entity_type`, `valid_start`, and `source_id` enable sub-millisecond graph queries.

---

## 2. Database Schema DDL (`resources/sqlite_db_schema.sql`)
- `ontology_nodes`: Stores GraphRAG Object Nodes with `valid_start` and `valid_end` temporal filtering.
- `ontology_edges`: Stores Kinetic Links with `kinetic_weight`, `friction_penalty`, and `confidence`.
- `user_memory`: Stores global shared user profile parameters.
- `decision_journal`: Stores historical user decision log entries.
- `surveillance_registry`: Stores active continuous risk surveillance targets.

---

## 3. High-Performance SQL Graph Operations
1. **Active Graph Retrieval**: SQL query retrieving active temporal sub-graphs for evaluation date $T_{\text{eval}}$:
   ```sql
   SELECT * FROM ontology_nodes WHERE valid_start <= T_eval AND (valid_end IS NULL OR valid_end >= T_eval);
   ```
2. **Surgical Poison Pruning**: Instantly purges compromised plugin nodes and edges via single SQL execution:
   ```sql
   DELETE FROM ontology_edges WHERE source_id = ?;
   DELETE FROM ontology_nodes WHERE source_id = ?;
   ```
