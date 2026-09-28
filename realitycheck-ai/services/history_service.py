"""
History Persistence Service for REALITYCHECK AI
Lightweight SQLite storage for saving and retrieving past investigations.
"""

import json
import sqlite3
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from config import DB_PATH

class HistoryService:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.init_db()

    def _get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Create history table if it doesn't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS investigations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    summary TEXT,
                    total_sources INTEGER DEFAULT 0,
                    total_claims INTEGER DEFAULT 0,
                    confidence_score INTEGER DEFAULT 0,
                    verdict TEXT,
                    payload JSON NOT NULL
                )
            """)
            conn.commit()

    def save_investigation(self, investigation_data: Dict[str, Any]) -> int:
        """Save a completed investigation to SQLite database."""
        question = investigation_data.get("question", "Untitled Query")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary = investigation_data.get("executive_summary", "")
        metrics = investigation_data.get("metrics", {})
        
        claims = investigation_data.get("claims", [])
        verdict = claims[0].get("status", "UNVERIFIED") if claims else "UNVERIFIED"

        payload_json = json.dumps(investigation_data)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO investigations 
                (question, timestamp, summary, total_sources, total_claims, confidence_score, verdict, payload)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                question,
                timestamp,
                summary,
                metrics.get("total_sources", 0),
                metrics.get("total_claims", 0),
                metrics.get("confidence_score", 0),
                verdict,
                payload_json
            ))
            conn.commit()
            return cursor.lastrowid

    def get_history(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Retrieve recent investigation history records."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, question, timestamp, summary, total_sources, total_claims, confidence_score, verdict
                FROM investigations
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_investigation_by_id(self, inv_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve full investigation details by database ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT payload FROM investigations WHERE id = ?", (inv_id,))
            row = cursor.fetchone()
            if row and row["payload"]:
                return json.loads(row["payload"])
        return None

    def delete_investigation(self, inv_id: int) -> bool:
        """Delete an investigation record by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM investigations WHERE id = ?", (inv_id,))
            conn.commit()
            return cursor.rowcount > 0
