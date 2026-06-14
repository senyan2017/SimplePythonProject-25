"""Tests for greeter.cli — argument parsing."""

import pytest

from greeter.cli import parse_args


class TestParseArgs:
    def test_no_args_all_none(self):
        args = parse_args([])
        assert args["name"] is None
        assert args["lang"] is None
        assert args["scene"] is None
        assert args["json"] is None

    def test_long_flags(self):
        args = parse_args(["--name", "Alice", "--lang", "ko", "--scene", "formal"])
        assert args["name"] == "Alice"
        assert args["lang"] == "ko"
        assert args["scene"] == "formal"

    def test_short_flags(self):
        args = parse_args(["-n", "Bob", "-l", "ja", "-s", "birthday"])
        assert args["name"] == "Bob"
        assert args["lang"] == "ja"
        assert args["scene"] == "birthday"

    def test_json_flag(self):
        args = parse_args(["--json"])
        assert args["json"] is True

    def test_invalid_lang_exits(self):
        with pytest.raises(SystemExit):
            parse_args(["--lang", "xx"])

    def test_invalid_scene_exits(self):
        with pytest.raises(SystemExit):
            parse_args(["--scene", "wedding"])

    def test_partial_args(self):
        args = parse_args(["--name", "Charlie"])
        assert args["name"] == "Charlie"
        assert args["lang"] is None
        assert args["scene"] is None


class TestEndToEndCLI:
    """Integration: CLI -> config -> core.run via main.main()."""

    def test_main_default(self):
        """main() with no args should succeed with defaults."""
        from main import main
        from unittest import mock
        import os

        with mock.patch("sys.argv", ["main.py"]):
            with mock.patch.dict(os.environ, {}, clear=True):
                code = main()
        assert code == 0

    def test_main_with_args(self):
        from main import main
        from unittest import mock
        import os

        with mock.patch("sys.argv", ["main.py", "--name", "Test", "--lang", "zh", "--scene", "newyear"]):
            with mock.patch.dict(os.environ, {}, clear=True):
                code = main()
        assert code == 0

    def test_main_invalid_input(self):
        """Passing an empty name via env should fail validation."""
        from main import main
        from unittest import mock
        import os

        with mock.patch("sys.argv", ["main.py"]):
            with mock.patch.dict(os.environ, {"GREETER_NAME": ""}, clear=True):
                code = main()
        assert code == 1

    def test_main_json_output(self):
        """--json flag should produce valid JSON on stdout."""
        import io
        import json
        import sys
        from unittest import mock
        import os
        from main import main

        captured = io.StringIO()
        with mock.patch("sys.argv", ["main.py", "--name", "JS", "--json"]):
            with mock.patch.dict(os.environ, {}, clear=True):
                old_stdout = sys.stdout
                sys.stdout = captured
                try:
                    code = main()
                finally:
                    sys.stdout = old_stdout
        assert code == 0
        data = json.loads(captured.getvalue())
        assert data["status"] == "success"
        assert data["data"]["name"] == "JS"
