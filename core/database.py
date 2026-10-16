"""
Vortex Database Engine (SQLite / Relational Schema)
Persistent storage for Render Jobs, Video Library, Viral Scripts, and YouTube Publishing Logs.
Built with WAL-mode concurrency and zero external dependencies.
"""

import os
import sqlite3
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger("VortexDB")

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vortex.db")

class Database:
    """Manages SQLite schema creation, CRUD operations, and transaction integrity."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")  # High concurrency
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def init_db(self):
        """Initializes relational schema with indexes."""
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. Video Jobs Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                topic TEXT NOT NULL,
                voice TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('queued', 'rendering', 'completed', 'failed')),
                progress INTEGER DEFAULT 0,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 2. Rendered Videos Catalog
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                job_id TEXT,
                topic TEXT NOT NULL,
                title TEXT NOT NULL,
                niche TEXT,
                language TEXT DEFAULT 'hi',
                duration REAL,
                size_mb REAL,
                resolution TEXT DEFAULT '1080x1920',
                video_path TEXT NOT NULL,
                metadata_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE SET NULL
            );
            """)

            # 3. YouTube Publishing Log
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id TEXT PRIMARY KEY,
                video_id TEXT NOT NULL,
                yt_video_id TEXT,
                yt_url TEXT,
                privacy_status TEXT NOT NULL CHECK(privacy_status IN ('private', 'unlisted', 'public')),
                published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
            );
            """)

            # Indexes for high performance lookup
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_videos_created ON videos(created_at DESC);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_uploads_video ON uploads(video_id);")

            conn.commit()

    # --- Job Operations ---
    def create_job(self, job_id: str, topic: str, voice: str) -> Dict[str, Any]:
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO jobs (id, topic, voice, status, progress) VALUES (?, ?, ?, 'queued', 0)",
                (job_id, topic, voice)
            )
            conn.commit()
        return self.get_job(job_id)

    def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: int = 0,
        error_message: Optional[str] = None
    ):
        with self._get_connection() as conn:
            conn.execute(
                """
                UPDATE jobs 
                SET status = ?, progress = ?, error_message = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (status, progress, error_message, job_id)
            )
            conn.commit()

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            if row:
                return dict(row)
        return None

    def list_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
            return [dict(r) for r in rows]

    # --- Video Operations ---
    def save_video(
        self,
        video_id: str,
        job_id: Optional[str],
        topic: str,
        title: str,
        duration: float,
        size_mb: float,
        video_path: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        meta_str = json.dumps(metadata or {}, ensure_ascii=False)
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO videos 
                (id, job_id, topic, title, duration, size_mb, video_path, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (video_id, job_id, topic, title, duration, size_mb, video_path, meta_str)
            )
            conn.commit()
        return self.get_video(video_id)

    def get_video(self, video_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM videos WHERE id = ?", (video_id,)).fetchone()
            if row:
                d = dict(row)
                if d.get("metadata_json"):
                    try:
                        d["metadata"] = json.loads(d["metadata_json"])
                    except json.JSONDecodeError:
                        d["metadata"] = {}
                return d
        return None

    def list_videos(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM videos ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
            results = []
            for r in rows:
                d = dict(r)
                if d.get("metadata_json"):
                    try:
                        d["metadata"] = json.loads(d["metadata_json"])
                    except Exception:
                        d["metadata"] = {}
                results.append(d)
            return results

    # --- Upload Operations ---
    def record_upload(
        self,
        upload_id: str,
        video_id: str,
        yt_video_id: Optional[str],
        yt_url: Optional[str],
        privacy_status: str
    ) -> Dict[str, Any]:
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO uploads (id, video_id, yt_video_id, yt_url, privacy_status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (upload_id, video_id, yt_video_id, yt_url, privacy_status)
            )
            conn.commit()
        return {"upload_id": upload_id, "video_id": video_id, "yt_url": yt_url, "status": privacy_status}
