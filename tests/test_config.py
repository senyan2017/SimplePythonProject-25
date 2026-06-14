"""Tests for configuration resolution (defaults, env vars, precedence)."""

from greeter.config import (
    Config,
    DEFAULT_LANGUAGE,
    DEFAULT_NAME,
    DEFAULT_SCENE,
    ENV_LANGUAGE,
    ENV_NAME,
    ENV_SCENE,
)


def test_defaults_when_no_env():
    cfg = Config.from_env(env={})
    assert cfg.name == DEFAULT_NAME
    assert cfg.language == DEFAULT_LANGUAGE
    assert cfg.scene == DEFAULT_SCENE


def test_from_env_reads_values():
    env = {ENV_NAME: "Bob", ENV_LANGUAGE: "ko", ENV_SCENE: "morning"}
    cfg = Config.from_env(env=env)
    assert cfg.name == "Bob"
    assert cfg.language == "ko"
    assert cfg.scene == "morning"


def test_resolve_cli_overrides_env():
    env = {ENV_NAME: "Bob", ENV_LANGUAGE: "ko", ENV_SCENE: "morning"}
    cfg = Config.resolve(name="Alice", language=None, scene="formal", env=env)
    assert cfg.name == "Alice"  # CLI wins
    assert cfg.language == "ko"  # falls back to env
    assert cfg.scene == "formal"  # CLI wins


def test_resolve_env_overrides_default():
    env = {ENV_LANGUAGE: "es"}
    cfg = Config.resolve(env=env)
    assert cfg.name == DEFAULT_NAME  # default
    assert cfg.language == "es"  # env
    assert cfg.scene == DEFAULT_SCENE  # default


def test_resolve_all_defaults_when_empty():
    cfg = Config.resolve(env={})
    assert (cfg.name, cfg.language, cfg.scene) == (
        DEFAULT_NAME,
        DEFAULT_LANGUAGE,
        DEFAULT_SCENE,
    )
