# User Experience Perfection & FTS5 Database Optimization

## 1. User Experience Critique: Addressing "Counter-Intuitive" Friction
To make LifeTree intuitive for non-technical users:

1. **Cognitive Jargon Translation (`scripts/human_translator.py`)**:
   - Converts raw math output (Dijkstra friction 4.22, Monte Carlo P90 31.8m, 95% VaR $18,508) into plain human executive summaries.
2. **Immediate Action Checklist (`scripts/action_checklist_generator.py`)**:
   - Translates complex multi-year graph routes into a clear, prioritized weekly to-do list with deadlines (`Within 7 Days`, `Within 14 Days`).
3. **Progressive Conversational Onboarding**:
   - Avoids overwhelming new users with 50-field JSON forms. Asks 3 initial questions (Goal, Role, Savings), generates the initial graph, and progressively asks for details as needed.

---

## 2. Advanced FTS5 Database Search & Concurrency Optimization (`scripts/sqlite_graph_store.py`)
- **FTS5 Virtual Table (`ontology_fts`)**: Indexed full-text search over node labels, properties, and entity types. Enables fuzzy search queries (e.g. "blocked account" or "blue card salary").
- **WAL Concurrency (`PRAGMA journal_mode=WAL;`)**: Enables multi-threaded reading and writing without database locks.
- **Online Backup (`backup_database`)**: Provides zero-downtime database backups.
