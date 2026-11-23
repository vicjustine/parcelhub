from parcelhub.db import connect, find_by_carrier, find_by_status, get_shipment
from parcelhub.seed import seed


def setup_module(module):
    seed()


def test_lookup_by_tracking_id():
    conn = connect()
    row = get_shipment(conn, "PH100000")
    assert row is not None
    assert row["tracking_id"] == "PH100000"


def test_find_by_carrier_returns_only_that_carrier():
    conn = connect()
    rows = find_by_carrier(conn, "northline")
    assert len(rows) > 0
    assert all(r["carrier"] == "northline" for r in rows)


def test_find_by_status_returns_only_that_status():
    conn = connect()
    rows = find_by_status(conn, "delivered")
    assert len(rows) > 0
    assert all(r["status"] == "delivered" for r in rows)


def test_unknown_carrier_returns_nothing():
    conn = connect()
    assert find_by_carrier(conn, "nosuchcarrier") == []
