"""Test suite for main.py.

It pins down the project's intended contract:
* ``greet()`` returns the right text and rejects bad input loudly.
* The CLI behaves identically whether run with no args, ``--name`` or ``-n``,
  and fails with a clear error on empty/whitespace names or unknown flags.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from main import greet

MAIN = str(Path(__file__).with_name("main.py"))


def run_cli(*args):
    """Run main.py as a subprocess and return the CompletedProcess."""
    return subprocess.run(
        [sys.executable, MAIN, *args],
        capture_output=True,
        text=True,
    )


class TestGreet:
    """Unit tests for the greet() function."""

    def test_default_greeting(self):
        assert greet() == "Let's Python Project"

    def test_greeting_with_name(self):
        result = greet("Alice")
        assert result == "Hello, Alice! Welcome to Let's Python Project"

    def test_greeting_strips_whitespace(self):
        result = greet("  Bob  ")
        assert result == "Hello, Bob! Welcome to Let's Python Project"

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            greet("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            greet("   ")

    def test_non_printable_raises(self):
        with pytest.raises(ValueError, match="invalid characters"):
            greet("Bad\x00Name")


class TestCLI:
    """Integration tests: run main.py as a subprocess to verify CLI behavior."""

    def test_no_args_prints_default(self):
        result = run_cli()
        assert result.returncode == 0
        assert "Let's Python Project" in result.stdout

    def test_name_arg(self):
        result = run_cli("--name", "World")
        assert result.returncode == 0
        assert "Hello, World! Welcome to Let's Python Project" in result.stdout

    def test_short_name_arg(self):
        result = run_cli("-n", "CLI")
        assert result.returncode == 0
        assert "Hello, CLI! Welcome to Let's Python Project" in result.stdout

    def test_empty_name_errors(self):
        result = run_cli("--name", "")
        assert result.returncode != 0
        assert "Error" in (result.stdout + result.stderr)

    def test_whitespace_name_errors(self):
        result = run_cli("--name", "   ")
        assert result.returncode != 0
        assert "Error" in (result.stdout + result.stderr)

    def test_unknown_flag_errors(self):
        result = run_cli("--unknown")
        assert result.returncode != 0
