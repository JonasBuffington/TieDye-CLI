"""
tiedye/logging.py

This module handles the analytics logging for the application.
It uses SQLite to store events in a database.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any

def _get_db_path() -> Path:
    """
    Constructs the path to the SQLite database file, ensuring the parent directory exists.
    """
    # The database will be stored in the same folder as templates
    db_dir = Path("~/.tiedye").expanduser()
    db_dir.mkdir(parents = True, exist_ok = True)
    return db_dir / "analytics.db"

def init_db():
    """
    Initializes the database and creates the 'events' table if it does not already exist.
    This is safe to run every time.
    """
    db_path = _get_db_path()
    # opens a connection to the db file
    con = sqlite3.connect(db_path)
    # a cursor is an object used to execute SQL commands
    cur = con.cursor()

    cur.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                details TEXT
                )
                """
                )
    
    con.commit()
    con.close()

def log_event(event_type: str, details: Dict[str, Any]):
    """
    Logs a new event to the database.

    Args:
        event_type: A string identifying the type of event (e.g., 'file_sorted').
        details: A dictionary containing event-specific metadata.
    """
    db_path = _get_db_path()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    timestamp = datetime.now(timezone.utc).isoformat()
    details_json = json.dumps(details)

    sql = "INSERT INTO events (timestamp, event_type, details) VALUES (?, ?, ?)"

    cur.execute(sql, (timestamp, event_type, details_json))

    con.commit()
    con.close()

init_db()
