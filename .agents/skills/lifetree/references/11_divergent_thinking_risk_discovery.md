# 11. Divergent Thinking Mode & Latent Risk Discovery Architecture

## 1. Executive Summary
Divergent Thinking Mode forces out-of-the-box latent risk discovery by evaluating active user decision topics against a multi-domain risk knowledge matrix across 5 distinct risk verticals:
1. **Tax Jurisdiction Exposure**: Exit tax liabilities, dual residence, worldwide income claims.
2. **Capital Control & Foreign Exchange Constraints**: Annual transfer limits, FX conversion bottlenecks.
3. **Statutory Healthcare Coverage Gaps**: Age cut-offs for public healthcare admission (>30 or >55 yo).
4. **Forced Heirship & Cross-Border Estate Probate Traps**: Statutory succession overrides under local civil codes.
5. **Dependent Age-Out Hazards**: Children approaching 18 or 21 during long-term PR processing.

---

## 2. Dynamic Risk Discovery Algorithm

$$\text{RiskScore}(R_k) = \text{SeverityWeight}(R_k) \times \sum_{c \in \text{Categories}} \mathbb{I}(c \in \text{UserProfile}) \times C(R_k)$$

Where:
- $\mathbb{I}(\cdot)$: Indicator function returning 1 if category match occurs.
- $C(R_k)$: Confidence score of the underlying risk knowledge node.

---

## 3. Surveillance Registry Schema

```sql
CREATE TABLE IF NOT EXISTS risk_surveillance_registry (
    domain_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    severity_level TEXT CHECK(severity_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    trigger_condition TEXT,
    tracking_metric TEXT,
    last_audited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Execution Pipeline Integration
Executes via [divergent_risk_discovery.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/risk_surveillance/divergent_risk_discovery.py) and updates [risk_surveillance_tracker.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/risk_surveillance/risk_surveillance_tracker.py).
