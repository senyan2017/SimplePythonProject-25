"""Tests for main.py — argument parsing and entry-point wiring."""

import pytest

from main import main, parse_args


class TestParseArgs:
    def test_defaults(self):
        args = parse_args([])
        assert args.name is None
        assert args.repeat == 1

    def test_name_flag(self):
        args = parse_args(["--name", "Alice"])
        assert args.name == "Alice"

    def test_repeat_flag(self):
        args = parse_args(["--repeat", "3"])
        assert args.repeat == 3

    def test_all_flags(self):
        args = parse_args(["--name", "Bob", "--repeat", "2"])
        assert args.name == "Bob"
        assert args.repeat == 2

    def test_invalid_repeat_exits(self):
        with pytest.raises(SystemExit):
            parse_args(["--repeat", "abc"])


class TestMain:
    def test_default_output(self, capsys):
        """main() with no args prints the standard welcome line."""
        main()
        out = capsys.readouterr().out
        assert out.strip() == "Welcome to Las's Python Project"

    def test_with_name(self, capsys):
        main(["--name", "Charlie"])
        out = capsys.readouterr().out
        assert "Hello, Charlie!" in out

    def test_repeat(self, capsys):
        main(["--repeat", "3"])
        out = capsys.readouterr().out
        lines = out.strip().splitlines()
        assert len(lines) == 3

    def test_repeat_with_name(self, capsys):
        main(["--name", "Dave", "--repeat", "2"])
        out = capsys.readouterr().out
        lines = out.strip().splitlines()
        assert len(lines) == 2
        assert all("Hello, Dave!" in line for line in lines)
