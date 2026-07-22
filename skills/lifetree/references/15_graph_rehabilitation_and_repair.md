# Graph Rehabilitation & Alternative Bridge Protocol

## 1. Overview
When a data plugin or source is revoked, `scripts/graph_confidence_filter.py` prunes the compromised sub-tree. However, simply pruning nodes leaves "broken decision paths" or orphan dependencies.

The **Graph Rehabilitation & Alternative Bridge Engine** (`scripts/graph_rehabilitation_engine.py`) automatically repairs damaged graphs:
1. **Broken Dependency Detection**: Identifies edges pointing to or from deleted poison nodes.
2. **Alternative Prerequisite Discovery**: Scans active candidate pool nodes for valid substitute prerequisites.
3. **Bridge Annotation**: Attaches "Repair Bridge" nodes with explicit `REPAIRED_BRIDGE` tags to restore valid decision pathways.

```
[Poison Node Pruned] ──(Leaves Broken Path)──> [scripts/graph_rehabilitation_engine.py]
                                                             │
                                                             ▼
                                             [Inject Alternative Valid Prerequisite]
                                                             │
                                                             ▼
                                             [Restored Intact Decision Pathway]
```
