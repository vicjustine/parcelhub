"""Runtime configuration loading."""

from __future__ import annotations

from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "settings.yml"


def load_config(path=None):
    """Read the service configuration from YAML."""
    target = Path(path) if path else CONFIG_PATH
    with open(target, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def carrier_endpoint(config, carrier):
    return config["carriers"][carrier]["endpoint"]
