"""Tests for the CLI entry point: defaults, overrides, env and error routing."""

import pytest

from greeter import cli
from greeter.config import ENV_LANGUAGE, ENV_NAME, ENV_SCENE, VERSION


def _clear_env(monkeypatch):
    for var in (ENV_NAME, ENV_LANGUAGE, ENV_SCENE):
        monkeypatch.delenv(var, raising=False)


def test_main_default(capsys, monkeypatch):
    _clear_env(monkeypatch)
    rc = cli.main([])
    captured = capsys.readouterr()
    assert rc == 0
    assert captured.out.strip() == "Hello, World!"
    assert captured.err == ""


def test_main_name_override(capsys, monkeypatch):
    _clear_env(monkeypatch)
    rc = cli.main(["--name", "Bob"])
    captured = capsys.readouterr()
    assert rc == 0
    assert captured.out.strip() == "Hello, Bob!"


def test_main_full_override(capsys, monkeypatch):
    _clear_env(monkeypatch)
    rc = cli.main(["-n", "Bob", "-l", "ko", "-s", "morning"])
    captured = capsys.readouterr()
    assert rc == 0
    assert captured.out.strip() == "좋은 아침이에요, Bob!"


def test_main_uses_env(capsys, monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv(ENV_NAME, "Eve")
    monkeypatch.setenv(ENV_LANGUAGE, "es")
    rc = cli.main([])
    captured = capsys.readouterr()
    assert rc == 0
    assert captured.out.strip() == "Hola, Eve!"


def test_cli_overrides_env(capsys, monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv(ENV_NAME, "Eve")
    rc = cli.main(["--name", "Bob"])
    captured = capsys.readouterr()
    assert rc == 0
    assert captured.out.strip() == "Hello, Bob!"


def test_invalid_language_goes_to_stderr(capsys, monkeypatch):
    _clear_env(monkeypatch)
    rc = cli.main(["--language", "xx"])
    captured = capsys.readouterr()
    assert rc == 2
    assert captured.out == ""  # nothing on stdout for a failure
    assert captured.err.startswith("error:")
    assert "UNSUPPORTED_LANGUAGE" in captured.err


def test_invalid_scene_returns_2(capsys, monkeypatch):
    _clear_env(monkeypatch)
    rc = cli.main(["--scene", "party"])
    captured = capsys.readouterr()
    assert rc == 2
    assert "UNSUPPORTED_SCENE" in captured.err


def test_empty_name_returns_2(capsys, monkeypatch):
    _clear_env(monkeypatch)
    rc = cli.main(["--name", "   "])
    captured = capsys.readouterr()
    assert rc == 2
    assert "EMPTY_NAME" in captured.err


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert VERSION in captured.out
