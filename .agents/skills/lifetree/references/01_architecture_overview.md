# LifeTree Architecture Overview

## 1. System Vision & Positioning
LifeTree (人生树) is a personal decision intelligence system (PDI) and personal decision operating system (Life OS) based on GraphRAG and a local-first privacy architecture. It is designed to assist users in high-risk, complex decision domains (global mobility, capital allocation, heavy medical choices, career pivots, tax optimization) by calculating causal paths, predicting geopolitical/legislative ripple effects, and building Plan B risk-hedging mechanisms.

## 2. Core Architectural Principles
- **Core Engine Closed-Source + Data Pipeline Open-Source + Local-First AI Native**:
  - **Open Data Connectors**: Public domain connectors are open-source, relying on standardized JSON schemas.
  - **Temporal GraphRAG**: Public knowledge graph stores temporal attributes (`Valid_Time`) and provenance (`Source_ID`).
  - **Local Sandbox Storage**: Core user memory and decision trees remain on the local device (SQLite / Vector DB). Supports complete offline operation.
  - **Federated Blinded Query**: When fetching global public graph data, the "Human-Machine Separation Protocol" obscures user identities so cloud servers cannot trace individual background.

```
[Open Connector Ecosystem] ──(Scrape & Clean)──> [Temporal GraphRAG Cloud Engine]
                                                        │
                                                        ▼
[User Local Terminal] <─────(Blinded Query)────── [Closed-Source Causal Engine]
   ├── Zero-Trust Encrypted Memory
   └── Generative Tree UI (GenUI)
```

## 3. Physical Decision Metaphor (The Soil, Tree, Topics, GenUI)
- **The Soil (Network)**: Temporal Knowledge Graph mapping global policies, statutes, and events.
- **The Tree**: User decision UI. Trunk = Current state; Main branches = Major decision paths; Side buds = Hypothetical What-If variables.
- **Topics**: Independent research topics (e.g., Global Mobility, Asset Allocation, Career Pivot, Health Strategy). Shared local memory with cross-topic ripple effect calculation.
- **Generative Tree UI (GenUI)**: Interactive tree UI replacing text-heavy output, highlighting optimal path, risk alerts (dead branch warnings), and Plan B alternatives.

## 4. Dual-Drive Engine Mechanism
1. **Short-Term Deep Research Framework**: One-off deep research engine generating full risk assessment reports.
2. **Medium/Long-Term Dynamic Monitoring**: High-frequency incremental polling engine that tracks temporal trends and triggers tiered event alerts (Daily briefing, Urgent SMS, In-app alerts).
