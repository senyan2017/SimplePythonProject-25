"""Tests for greeter.config — environment variables and defaults."""

import os
from unittest import mock

import pytest

from greeter.config import DEFAULTS, load_config


class TestLoadConfigDefaults:
    """When no CLI args and no env vars, defaults should apply."""

    def test_all_defaults(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            cfg = load_config({})
        assert cfg["name"] == DEFAULTS["name"]
        assert cfg["lang"] == DEFAULTS["lang"]
        assert cfg["scene"] == DEFAULTS["scene"]
        assert cfg["json"] == DEFAULTS["json"]

    def test_none_cli_args_use_defaults(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            cfg = load_config({"name": None, "lang": None, "scene": None, "json": None})
        assert cfg["name"] == DEFAULTS["name"]


class TestLoadConfigEnvVars:
    """Environment variables should override defaults."""

    def test_env_name(self):
        with mock.patch.dict(os.environ, {"GREETER_NAME": "EnvUser"}, clear=True):
            cfg = load_config({})
        assert cfg["name"] == "EnvUser"

    def test_env_lang(self):
        with mock.patch.dict(os.environ, {"GREETER_LANG": "ko"}, clear=True):
            cfg = load_config({})
        assert cfg["lang"] == "ko"

    def test_env_scene(self):
        with mock.patch.dict(os.environ, {"GREETER_SCENE": "birthday"}, clear=True):
            cfg = load_config({})
        assert cfg["scene"] == "birthday"

    def test_env_json_true(self):
        with mock.patch.dict(os.environ, {"GREETER_JSON": "true"}, clear=True):
            cfg = load_config({})
        assert cfg["json"] is True

    def test_env_json_false(self):
        with mock.patch.dict(os.environ, {"GREETER_JSON": "false"}, clear=True):
            cfg = load_config({})
        assert cfg["json"] is False

    def test_env_json_numeric(self):
        with mock.patch.dict(os.environ, {"GREETER_JSON": "1"}, clear=True):
            cfg = load_config({})
        assert cfg["json"] is True


class TestLoadConfigCliOverrides:
    """CLI args should take highest priority."""

    def test_cli_overrides_env(self):
        with mock.patch.dict(os.environ, {"GREETER_NAME": "EnvUser"}, clear=True):
            cfg = load_config({"name": "CliUser", "lang": None, "scene": None, "json": None})
        assert cfg["name"] == "CliUser"

    def test_cli_overrides_all(self):
        with mock.patch.dict(
            os.environ,
            {"GREETER_NAME": "E", "GREETER_LANG": "ko", "GREETER_SCENE": "formal"},
            clear=True,
        ):
            cfg = load_config({"name": "C", "lang": "ja", "scene": "birthday", "json": True})
        assert cfg["name"] == "C"
        assert cfg["lang"] == "ja"
        assert cfg["scene"] == "birthday"
        assert cfg["json"] is True

    def test_partial_cli_fills_from_env_then_default(self):
        with mock.patch.dict(os.environ, {"GREETER_LANG": "zh"}, clear=True):
            cfg = load_config({"name": "Alice", "lang": None, "scene": None, "json": None})
        assert cfg["name"] == "Alice"  # from CLI
        assert cfg["lang"] == "zh"     # from env
        assert cfg["scene"] == DEFAULTS["scene"]  # from default
