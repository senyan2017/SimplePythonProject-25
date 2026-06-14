"""Configuration layer: environment variables + defaults."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

# Default values used when neither CLI args nor env vars are set.
DEFAULTS: Dict[str, Any] = {
    "name": "World",
    "lang": "en",
    "scene": "casual",
    "json": False,
}

# Mapping: config key -> environment variable name
ENV_KEYS: Dict[str, str] = {
    "name": "GREETER_NAME",
    "lang": "GREETER_LANG",
    "scene": "GREETER_SCENE",
    "json": "GREETER_JSON",
}


def load_config(cli_overrides: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Build effective configuration.

    Priority (highest to lowest):
      1. Explicit CLI overrides (non-None values)
      2. Environment variables
      3. Hard-coded defaults

    Args:
        cli_overrides: dict from argparse (may contain None for unset args).

    Returns:
        dict with keys: name, lang, scene, json
    """
    cli = cli_overrides or {}
    config = {}

    for key, default in DEFAULTS.items():
        # 1. CLI override wins if explicitly provided (not None)
        cli_val = cli.get(key)
        if cli_val is not None:
            config[key] = cli_val
            continue

        # 2. Environment variable
        env_var = ENV_KEYS[key]
        env_val = os.environ.get(env_var)
        if env_val is not None:
            config[key] = _cast(key, env_val, default)
            continue

        # 3. Default
        config[key] = default

    return config


def _cast(key: str, raw: str, default: Any) -> Any:
    """Cast a raw environment variable string to the correct type."""
    if isinstance(default, bool):
        return raw.lower() in ("1", "true", "yes", "on")
    return raw
