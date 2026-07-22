# Shared User Memory & Decision Journal Architecture

## 1. Shared Asset Concept
In LifeTree, **User Memory** is a shared, persistent asset (`resources/user_global_memory_store.json`) maintained across all active research topics:
- **Global Profile**: Age, nationality, degrees, language certifications, work history, and liquid financial assets. Modifying any baseline parameter once automatically syncs across all research topics.
- **Explicit Goals & Requirements**: High-level strategic targets (e.g. "Achieve EU Dual Status in 3 Years").
- **Decision Journal (决策日志)**: Historical log recording user choices, selected pathways, decision rationale, and Plan B trigger status over time.

---

## 2. Dynamic Memory Update Pipeline (`scripts/user_memory_manager.py`)
1. **User Input / Feedback**: When the user states new information (e.g. "I passed German B1 test") or makes a decision ("I select Option A"), the Agent invokes `scripts/user_memory_manager.py`.
2. **Profile Mutation**: Baseline profile parameters update instantly and sync across active topics.
3. **Decision Journaling**: Appends a permanent decision log entry with timestamp and chosen pathway.
4. **Graph Re-evaluation**: Triggers `scripts/rule_evaluator_engine.py` and `scripts/decision_tree_engine.py` to re-render decision tree models.
