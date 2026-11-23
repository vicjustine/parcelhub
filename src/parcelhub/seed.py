"""Generate the synthetic shipment dataset."""

from __future__ import annotations

import random

from .db import connect, init_schema

CARRIERS = ["northline", "velocity", "harbourway"]
STATUSES = ["in_transit", "delivered", "exception", "pending_pickup"]
CITIES = ["Toronto", "Vancouver", "Montreal", "Calgary", "Halifax", "Winnipeg"]
CUSTOMERS = [
    "Mapleline Goods", "Northfield Supply", "Harbour Co-op",
    "Prairie Outfitters", "Lakeshore Trading", "Summit Components",
]


def seed(count=240, rng_seed=20261122):
    rng = random.Random(rng_seed)
    conn = connect()
    init_schema(conn)
    conn.execute("DELETE FROM shipments")
    rows = []
    for i in range(count):
        rows.append((
            f"PH{100000 + i}",
            rng.choice(CARRIERS),
            rng.choice(CITIES),
            rng.choice(CITIES),
            rng.choice(STATUSES),
            round(rng.uniform(0.4, 48.0), 2),
            rng.choice(CUSTOMERS),
        ))
    conn.executemany(
        "INSERT INTO shipments VALUES (?, ?, ?, ?, ?, ?, ?)", rows
    )
    conn.commit()
    return len(rows)


if __name__ == "__main__":
    print(f"seeded {seed()} shipments")
