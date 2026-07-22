#!/usr/bin/env python3
"""
LifeTree Embedded Local SQLite Database Manager (FTS5 & Backup Enhanced)
Provides zero-dependency, high-performance local SQLite storage with FTS5 Full-Text Search,
WAL mode concurrency, automatic backup, and graph query methods.
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Path resolution relative to module position: scripts/graph_engines/sqlite_graph_store.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

DEFAULT_DB_PATH = os.path.join(SKILL_ROOT, "resources", "database", "lifetree_local_db.sqlite")
SCHEMA_SQL_PATH = os.path.join(SKILL_ROOT, "resources", "database", "sqlite_db_schema.sql")

class LifeTreeSQLiteStore:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        if os.path.exists(SCHEMA_SQL_PATH):
            with open(SCHEMA_SQL_PATH, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            self.conn.executescript(schema_sql)
            self.conn.commit()

    def upsert_node(self, node: Dict[str, Any]) -> str:
        now_iso = datetime.now(timezone.utc).isoformat()
        nid = node.get("id")
        label = node.get("label", "Unnamed")
        etype = node.get("entity_type", "POLICY_LAW")
        props = json.dumps(node.get("properties", {}))
        vt = node.get("valid_time", {})
        vstart = vt.get("start_time", now_iso)
        vend = vt.get("end_time")
        source_id = node.get("source_id", "SRC_UNKNOWN")
        source_url = node.get("source_url")
        conf = float(node.get("confidence", 1.0))

        sql = """
        INSERT INTO ontology_nodes (id, label, entity_type, properties_json, valid_start, valid_end, source_id, source_url, confidence, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            label=excluded.label,
            entity_type=excluded.entity_type,
            properties_json=excluded.properties_json,
            valid_start=excluded.valid_start,
            valid_end=excluded.valid_end,
            source_id=excluded.source_id,
            source_url=excluded.source_url,
            confidence=excluded.confidence,
            updated_at=excluded.updated_at
        """
        self.conn.execute(sql, (nid, label, etype, props, vstart, vend, source_id, source_url, conf, now_iso, now_iso))
        self.conn.commit()
        return nid

    def upsert_edge(self, edge: Dict[str, Any]) -> str:
        now_iso = datetime.now(timezone.utc).isoformat()
        s = edge.get("source")
        t = edge.get("target")
        eid = edge.get("id", f"edge_{s}_{t}")
        rel = edge.get("relation_type", "IMPACTS")
        w = float(edge.get("kinetic_weight", 1.0))
        f = float(edge.get("friction_penalty", 0.0))
        source_id = edge.get("source_id", "SRC_UNKNOWN")
        conf = float(edge.get("confidence", 1.0))

        sql = """
        INSERT INTO ontology_edges (id, source_node, target_node, relation_type, kinetic_weight, friction_penalty, source_id, confidence, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            kinetic_weight=excluded.kinetic_weight,
            friction_penalty=excluded.friction_penalty,
            confidence=excluded.confidence
        """
        self.conn.execute(sql, (eid, s, t, rel, w, f, source_id, conf, now_iso))
        self.conn.commit()
        return eid

    def fts_search_nodes(self, query_text: str, limit: int = 10) -> List[Dict[str, Any]]:
        sql = """
        SELECT n.*, fts.rank
        FROM ontology_fts fts
        JOIN ontology_nodes n ON n.id = fts.id
        WHERE ontology_fts MATCH ?
        ORDER BY fts.rank
        LIMIT ?
        """
        cursor = self.conn.execute(sql, (query_text, limit))
        results = []
        for r in cursor.fetchall():
            results.append({
                "id": r["id"],
                "label": r["label"],
                "entity_type": r["entity_type"],
                "properties": json.loads(r["properties_json"]) if r["properties_json"] else {},
                "valid_time": {"start_time": r["valid_start"], "end_time": r["valid_end"]},
                "source_id": r["source_id"],
                "confidence": r["confidence"],
                "fts_rank": r["rank"]
            })
        return results

    def query_active_graph(self, eval_time_iso: Optional[str] = None) -> Dict[str, Any]:
        eval_time = eval_time_iso or datetime.now(timezone.utc).isoformat()
        
        node_sql = """
        SELECT * FROM ontology_nodes
        WHERE valid_start <= ? AND (valid_end IS NULL OR valid_end >= ?)
        """
        cursor = self.conn.execute(node_sql, (eval_time, eval_time))
        nodes = []
        for r in cursor.fetchall():
            nodes.append({
                "id": r["id"],
                "label": r["label"],
                "entity_type": r["entity_type"],
                "properties": json.loads(r["properties_json"]) if r["properties_json"] else {},
                "valid_time": {"start_time": r["valid_start"], "end_time": r["valid_end"]},
                "source_id": r["source_id"],
                "confidence": r["confidence"]
            })

        active_node_ids = {n["id"] for n in nodes}
        
        edge_sql = "SELECT * FROM ontology_edges"
        cursor = self.conn.execute(edge_sql)
        edges = []
        for r in cursor.fetchall():
            if r["source_node"] in active_node_ids and r["target_node"] in active_node_ids:
                edges.append({
                    "id": r["id"],
                    "source": r["source_node"],
                    "target": r["target_node"],
                    "relation_type": r["relation_type"],
                    "kinetic_weight": r["kinetic_weight"],
                    "friction_penalty": r["friction_penalty"],
                    "source_id": r["source_id"],
                    "confidence": r["confidence"]
                })

        return {"nodes": nodes, "edges": edges}

    def prune_poison_source_sql(self, revoked_source_id: str) -> Dict[str, Any]:
        cursor_edges = self.conn.execute("DELETE FROM ontology_edges WHERE source_id = ?", (revoked_source_id,))
        deleted_edges = cursor_edges.rowcount

        cursor_nodes = self.conn.execute("DELETE FROM ontology_nodes WHERE source_id = ?", (revoked_source_id,))
        deleted_nodes = cursor_nodes.rowcount
        
        self.conn.commit()

        return {
            "sql_pruning_summary": {
                "revoked_source_id": revoked_source_id,
                "deleted_nodes_count": deleted_nodes,
                "deleted_edges_count": deleted_edges,
                "db_status": "POISON_NODES_PURGED"
            }
        }

    def backup_database(self, target_backup_path: str) -> Dict[str, Any]:
        os.makedirs(os.path.dirname(target_backup_path), exist_ok=True)
        backup_conn = sqlite3.connect(target_backup_path)
        self.conn.backup(backup_conn)
        backup_conn.close()

        return {
            "backup_summary": {
                "backup_file_path": target_backup_path,
                "status": "BACKUP_SUCCESSFUL",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }

    def close(self):
        self.conn.close()

def main():
    store = LifeTreeSQLiteStore()
    
    store.upsert_node({
        "id": "node_fts_test_01",
        "label": "€12,000 Blocked Deposit Account (Sperrknto)",
        "entity_type": "CAPITAL_ASSET",
        "properties": {"currency": "EUR", "amount": 12000},
        "source_id": "SRC_FTS_TEST",
        "confidence": 1.0
    })

    fts_results = store.fts_search_nodes("Blocked Account")
    
    backup_file = os.path.join(os.path.dirname(DEFAULT_DB_PATH), "lifetree_db_backup.sqlite")
    backup_res = store.backup_database(backup_file)

    store.prune_poison_source_sql("SRC_FTS_TEST")
    store.close()

    print(json.dumps({
        "fts_search_results_count": len(fts_results),
        "fts_match_label": fts_results[0]["label"] if fts_results else None,
        "backup_result": backup_res
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
