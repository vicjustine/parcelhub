"""Proof that carrier/status lookups resist SQL injection.

These are the regression tests for the CodeQL py/sql-injection findings.
"""

from parcelhub.db import connect, find_by_carrier, find_by_status
from parcelhub.seed import seed


def setup_module(module):
    seed()


def test_carrier_lookup_resists_injection():
    conn = connect()
    rows = find_by_carrier(conn, "nosuch' OR '1'='1")
    assert rows == [], "injected predicate returned rows"


def test_status_lookup_resists_injection():
    conn = connect()
    rows = find_by_status(conn, "nosuch' OR '1'='1")
    assert rows == [], "injected predicate returned rows"
