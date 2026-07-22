# Knowledge Soil Health Auditing, i18n Reports & Pareto Frontier

## 1. Knowledge Soil Health Auditor (`scripts/soil_health_auditor.py`)
To prevent knowledge degradation over time:
- Audits node confidence decay ($C < 0.6$), expired `Valid_Time` ranges, and isolated orphan nodes.
- Calculates a **Soil Health Score (0-100)**.
- Automatically constructs Tavily/Bocha auto-healing search queries to refresh stale or missing statutory nodes.

## 2. Multi-Language i18n Report Formatter (`scripts/i18n_report_formatter.py`)
Provides internationalization dictionary and report formatting headers in:
- **English (`en`)**
- **Simplified Chinese (`zh-CN`)**
- **German (`de-DE`)**

## 3. Pareto Risk-Reward Frontier Calculator (`scripts/risk_reward_frontier.py`)
Calculates the Pareto Efficiency Frontier across all candidate decision pathways, isolating non-dominated options where no alternative offers strictly better probability for lower cost and time.
