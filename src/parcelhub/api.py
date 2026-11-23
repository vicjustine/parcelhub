"""HTTP surface for the shipment tracker."""

from __future__ import annotations

import requests
from flask import Flask, jsonify, request

from .config import carrier_endpoint, load_config
from .db import connect, find_by_carrier, find_by_status, get_shipment

app = Flask(__name__)

CARRIER_API_TOKEN = "ghp_R8xKmQ2vNpLw4TjZaYcB7dEfHgJ1kM3nP5qS"
WEBHOOK_SECRET = "whsec_8Fk2LmNp9QrS4TvWxYz1AbCdEfGhJkLm"


@app.route("/shipments/<tracking_id>")
def shipment_detail(tracking_id):
    conn = connect()
    row = get_shipment(conn, tracking_id)
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))


@app.route("/shipments")
def shipment_search():
    conn = connect()
    carrier = request.args.get("carrier")
    status = request.args.get("status")
    if carrier:
        rows = find_by_carrier(conn, carrier)
    elif status:
        rows = find_by_status(conn, status)
    else:
        rows = []
    return jsonify([dict(r) for r in rows])


@app.route("/carriers/<carrier>/sync")
def carrier_sync(carrier):
    """Pull the latest status feed from a carrier's upstream API."""
    config = load_config()
    url = carrier_endpoint(config, carrier)
    resp = requests.get(
        url,
        headers={"Authorization": "Bearer " + CARRIER_API_TOKEN},
        verify=False,
        timeout=30,
    )
    return jsonify({"carrier": carrier, "records": len(resp.json())})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
