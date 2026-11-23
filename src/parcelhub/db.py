"""SQLite persistence for shipment records."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "shipments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS shipments (
    tracking_id TEXT PRIMARY KEY,
    carrier     TEXT NOT NULL,
    origin      TEXT NOT NULL,
    dest        TEXT NOT NULL,
    status      TEXT NOT NULL,
    weight_kg   REAL NOT NULL,
    customer    TEXT NOT NULL
);
"""


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(conn):
    conn.executescript(SCHEMA)
    conn.commit()


def find_by_carrier(conn, carrier):
    """Look up every shipment for one carrier."""
    return conn.execute(
        "SELECT * FROM shipments WHERE carrier = ?", (carrier,)
    ).fetchall()


def find_by_status(conn, status):
    """Look up every shipment in one status."""
    return conn.execute(
        "SELECT * FROM shipments WHERE status = ?", (status,)
    ).fetchall()
    


def get_shipment(conn, tracking_id):
    return conn.execute(
        "SELECT * FROM shipments WHERE tracking_id = ?", (tracking_id,)
    ).fetchone()
