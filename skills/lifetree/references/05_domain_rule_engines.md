# LifeTree Domain Rule Engines & Plugin Architecture

## 1. Domain-Agnostic Modular Engine System
LifeTree does not hardcode any single country or industry rules. Instead, it operates a universal **Domain Rule Engine** (`scripts/rule_evaluator_engine.py`) that loads standardized domain JSON rule packs (`resources/domain_rule_schema.json`).

Supported decision domains include, but are not limited to:
- **Global Mobility & Immigration**: Points-based visas, golden visas, skilled worker pathways, talent residence.
- **Asset Allocation & Wealth Preservation**: Cross-border liquidity management, risk-hedging portfolios, tax efficiency.
- **Career Pivot & Executive Strategy**: Industry transitions, skill qualification match, salary threshold audits.
- **Heavy Medical Decisions**: Multi-treatment pathway evaluation, clinical risk/benefit trade-offs.
- **Tax & Regulatory Optimization**: Cross-jurisdiction compliance and statutory reporting.

---

## 2. Structure of a LifeTree Domain Rule Pack

A domain rule pack consists of four core evaluation blocks:

1. **Prerequisites Block**: Hard requirements (boolean flags, qualification degrees, background clearance).
2. **Point Scoring Block**: Dynamic point grids (age brackets, language levels, experience tiers).
3. **Threshold Checks Block**: Financial liquidity, annual income, debt-to-income limits with severity ratings (`CRITICAL`, `HIGH`, `MEDIUM`).
4. **Timeline Milestones Block**: Progressive status advancement markers.

---

## 3. Plug-and-Play Rule Templates
Developers and users can create new domain packs by supplying a JSON conforming to `resources/domain_rule_schema.json`. See `examples/domain_templates/` for example rule packs.
