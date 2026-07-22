# Agentic Dynamic Data Ingestion & JIT Connectors

## 1. Paradigm Shift: Agent as Universal Connector
In traditional software, integration requires hardcoding static scrapers, maintaining plugin manifests, and building developer payout systems.

In an **Agent-First Skill Paradigm**, static connectors are redundant. The AI Agent acts as the **Universal Dynamic Data Connector**:
- **On-the-Fly Scraping & Extraction**: Upon user request or when encountering a new web page, PDF, or API, the Agent fetches the raw content dynamically using web tools.
- **JIT Extraction to Core Ontology**: The Agent normalizes raw unstructured data on-the-fly into standardized `nodes` and `edges` using `scripts/jit_connector_synthesizer.py`.
- **Automatic Provenance & Confidence**: The Agent auto-hashes the source URL to form a deterministic `Source_ID`, assigns `Valid_Time` scope, and tags initial confidence scores (`1.0` Official, `0.8` Community, `0.5` Model Prediction).

```
[Raw Unstructured Source] (Web URL / PDF / API)
          │
          ▼
[AI Agent JIT Processing] ──(Extract Facts & Entities)──> [scripts/jit_connector_synthesizer.py]
                                                                      │
                                                                      ▼
                                                      [Standardized GraphRAG Payload]
```

## 2. Ingestion Prompt Directives for AI Agents
When encountering any raw information source, the Agent executes the following 4-step pipeline:

1. **Extract Core Entities**: Identify policies, requirements, roles, financial figures, fees, and deadlines. Assign `entity_type` (`POLICY_LAW`, `FEES_REQUIREMENT`, `IMMIGRATION_ROUTE`, `CAREER_ROLE`, `TIMELINE_EVENT`, `RISK_NODE`, `WHAT_IF_HYPOTHESIS`).
2. **Extract Relations**: Identify causal dependencies (`REQUIRES`, `PREREQUISITE_FOR`, `IMPACTS`, `RISK_OF`, `CONVERTS_TO`, `CONFLICTS_WITH`).
3. **Set Temporal Scope**: Inspect text for effective dates or amendment timestamps (`Valid_Time.start_time`, `Valid_Time.end_time`).
4. **Synthesize Payload**: Invoke `scripts/jit_connector_synthesizer.py` to produce clean nodes and edges for the decision tree solver.
