-- LifeTree Embedded Local SQLite Database Schema (FTS5 & WAL Optimized)

PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS ontology_nodes (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    properties_json TEXT,
    valid_start TEXT NOT NULL,
    valid_end TEXT,
    source_id TEXT NOT NULL,
    source_url TEXT,
    confidence REAL NOT NULL DEFAULT 1.0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ontology_edges (
    id TEXT PRIMARY KEY,
    source_node TEXT NOT NULL,
    target_node TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    kinetic_weight REAL DEFAULT 1.0,
    friction_penalty REAL DEFAULT 0.0,
    source_id TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 1.0,
    created_at TEXT NOT NULL,
    FOREIGN KEY(source_node) REFERENCES ontology_nodes(id) ON DELETE CASCADE,
    FOREIGN KEY(target_node) REFERENCES ontology_nodes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_memory (
    user_id TEXT PRIMARY KEY,
    profile_json TEXT NOT NULL,
    goals_json TEXT,
    last_updated TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS decision_journal (
    entry_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    decision_title TEXT NOT NULL,
    chosen_pathway TEXT NOT NULL,
    user_rationale TEXT,
    plan_b_status TEXT DEFAULT 'INACTIVE'
);

CREATE TABLE IF NOT EXISTS surveillance_registry (
    risk_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT,
    tracking_metric TEXT,
    first_discovered_at TEXT NOT NULL,
    last_checked_at TEXT NOT NULL,
    surveillance_status TEXT DEFAULT 'ACTIVE_SURVEILLANCE'
);

-- B-Tree Indexes for Fast Graph Queries
CREATE INDEX IF NOT EXISTS idx_nodes_entity_type ON ontology_nodes(entity_type);
CREATE INDEX IF NOT EXISTS idx_nodes_source_id ON ontology_nodes(source_id);
CREATE INDEX IF NOT EXISTS idx_nodes_valid_start ON ontology_nodes(valid_start);
CREATE INDEX IF NOT EXISTS idx_edges_source ON ontology_edges(source_node);
CREATE INDEX IF NOT EXISTS idx_edges_target ON ontology_edges(target_node);
CREATE INDEX IF NOT EXISTS idx_edges_relation ON ontology_edges(relation_type);

-- FTS5 Virtual Table for High-Performance Full-Text Search over Nodes
CREATE VIRTUAL TABLE IF NOT EXISTS ontology_fts USING fts5(
    id UNINDEXED,
    label,
    entity_type,
    properties_json,
    content='ontology_nodes',
    content_rowid='rowid'
);

-- Triggers to Keep FTS5 Index Auto-Synced with Primary Node Table
CREATE TRIGGER IF NOT EXISTS ontology_nodes_ai AFTER INSERT ON ontology_nodes BEGIN
  INSERT INTO ontology_fts(rowid, id, label, entity_type, properties_json)
  VALUES (new.rowid, new.id, new.label, new.entity_type, new.properties_json);
END;

CREATE TRIGGER IF NOT EXISTS ontology_nodes_ad AFTER DELETE ON ontology_nodes BEGIN
  INSERT INTO ontology_fts(ontology_fts, rowid, id, label, entity_type, properties_json)
  VALUES('delete', old.rowid, old.id, old.label, old.entity_type, old.properties_json);
END;

CREATE TRIGGER IF NOT EXISTS ontology_nodes_au AFTER UPDATE ON ontology_nodes BEGIN
  INSERT INTO ontology_fts(ontology_fts, rowid, id, label, entity_type, properties_json)
  VALUES('delete', old.rowid, old.id, old.label, old.entity_type, old.properties_json);
  INSERT INTO ontology_fts(rowid, id, label, entity_type, properties_json)
  VALUES (new.rowid, new.id, new.label, new.entity_type, new.properties_json);
END;
