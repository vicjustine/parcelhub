"""Security regression: carrier and status lookups must not be injectable.

Written against CodeQL alerts py/sql-injection at db.py:37 and db.py:43.
"""

from parcelhub.db import connect, find_by_carrier, find_by_status
from parcelhub.seed import seed

INJECTION = "nosuch' OR '1'='1"


def setup_module(module):
    seed()


def test_carrier_lookup_resists_injection():
    conn = connect()
    rows = find_by_carrier(conn, INJECTION)
    assert rows == [], (
        f"SQL injection succeeded: a carrier that does not exist returned "
        f"{len(rows)} rows (the entire shipments table)"
    )


def test_status_lookup_resists_injection():
    conn = connect()
    rows = find_by_status(conn, INJECTION)
    assert rows == [], (
        f"SQL injection succeeded: a status that does not exist returned "
        f"{len(rows)} rows (the entire shipments table)"
    )
