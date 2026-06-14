import subprocess
import sys

import pytest

from main import greet


class TestGreet:
    """Unit tests for the greet() function."""

    def test_default_greeting(self):
        assert greet() == "Let's Python Project"

    def test_greeting_with_name(self):
        result = greet("Alice")
        assert result == "Hello, Alice! Welcome to Let's Python Project"

    def test_greeting_strips_whitespace(self):
        assert greet("  Bob  ") == "Hello, Bob! Welcome to Let's Python Project"

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

    def _run(self, *args):
        return subprocess.run(
            [sys.executable, "main.py", *args],
            capture_output=True,
            text=True,
        )

    def test_no_args_prints_default(self):
        result = self._run()
        assert result.returncode == 0
        assert result.stdout.strip() == "Let's Python Project"

    def test_name_arg(self):
        result = self._run("--name", "World")
        assert result.returncode == 0
        assert result.stdout.strip() == "Hello, World! Welcome to Let's Python Project"

    def test_short_name_arg(self):
        result = self._run("-n", "CLI")
        assert result.returncode == 0
        assert result.stdout.strip() == "Hello, CLI! Welcome to Let's Python Project"

    def test_empty_name_errors(self):
        result = self._run("--name", "")
        assert result.returncode != 0
        assert "Error" in result.stderr

    def test_whitespace_name_errors(self):
        result = self._run("--name", "   ")
        assert result.returncode != 0
        assert "Error" in result.stderr

    def test_unknown_flag_errors(self):
        result = self._run("--unknown")
        assert result.returncode != 0
