# Incremental Diff Engine & Tiered Push Alert Architecture

## 1. Zero-Resource Silent Polling (Diff Engine)
To prevent push fatigue and conserve compute/notification resources:
- The system regularly polls monitored sources via `scripts/event_push_diff_engine.py`.
- **Zero-Diff Silent Mode**: When no policy or graph data changes occur, the engine remains 100% silent (0 notification resources consumed).

## 2. Tiered Event-Driven Push Dispatch
When a diff is detected, changes are categorized into a 3-tier severity matrix:

| Severity | Event Type | Dispatch Channel | Action Required |
| :--- | :--- | :--- | :--- |
| **LOW / MEDIUM** | Minor guideline updates, routine processing time shifts, typo fixes | **Daily / Weekly Brief Queue** | Batched and dispatched in user-selected daily/weekly digest (App / Email). |
| **HIGH / CRITICAL** | Statutory policy suspensions, sharp quota reductions, blocked account limit increases | **Urgent Circuit Breaker Alert** | Triggers instant SMS or High-Priority Push Notification to bring the user back immediately. |

```
[Incremental Polling] ──> [Diff Engine] ──(No Diff?)──> [100% Silent]
                                │
                           (Diff Found)
                                │
       ┌────────────────────────┴────────────────────────┐
       ▼                                                 ▼
[Low/Med Severity]                               [High/Critical Severity]
       │                                                 │
[Daily/Weekly Brief Queue]                       [Urgent SMS / High-Priority Push]
```
