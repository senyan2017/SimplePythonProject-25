"""Tests for greeter.core — greeting logic and output formatting."""

import io
import json

import pytest

from greeter.core import (
    SUPPORTED_LANGS,
    SUPPORTED_SCENES,
    format_error,
    format_success,
    generate_greeting,
    run,
    validate_inputs,
)


# ── validate_inputs ──────────────────────────────────────────────


class TestValidateInputs:
    def test_valid_inputs(self):
        assert validate_inputs("Alice", "en", "casual") is None

    def test_empty_name(self):
        err = validate_inputs("", "en", "casual")
        assert err is not None
        assert "empty" in err.lower()

    def test_whitespace_only_name(self):
        err = validate_inputs("   ", "en", "casual")
        assert err is not None

    def test_unsupported_lang(self):
        err = validate_inputs("Alice", "fr", "casual")
        assert err is not None
        assert "fr" in err

    def test_unsupported_scene(self):
        err = validate_inputs("Alice", "en", "wedding")
        assert err is not None
        assert "wedding" in err

    @pytest.mark.parametrize("lang", SUPPORTED_LANGS)
    def test_all_supported_langs(self, lang):
        assert validate_inputs("Test", lang, "casual") is None

    @pytest.mark.parametrize("scene", SUPPORTED_SCENES)
    def test_all_supported_scenes(self, scene):
        assert validate_inputs("Test", "en", scene) is None


# ── generate_greeting ────────────────────────────────────────────


class TestGenerateGreeting:
    def test_english_casual(self):
        g = generate_greeting("Alice", "en", "casual")
        assert "Alice" in g

    def test_korean_formal(self):
        g = generate_greeting("민수", "ko", "formal")
        assert "민수" in g

    def test_chinese_birthday(self):
        g = generate_greeting("小明", "zh", "birthday")
        assert "小明" in g
        assert "生日" in g

    def test_japanese_newyear(self):
        g = generate_greeting("太郎", "ja", "newyear")
        assert "太郎" in g

    def test_name_is_stripped(self):
        g = generate_greeting("  Bob  ", "en", "casual")
        assert "  Bob  " not in g
        assert "Bob" in g

    @pytest.mark.parametrize("lang", SUPPORTED_LANGS)
    @pytest.mark.parametrize("scene", SUPPORTED_SCENES)
    def test_all_combinations_produce_output(self, lang, scene):
        g = generate_greeting("Tester", lang, scene)
        assert isinstance(g, str)
        assert len(g) > 0


# ── format_success ───────────────────────────────────────────────


class TestFormatSuccess:
    def test_plain_text(self):
        out = format_success("Alice", "en", "casual", "Hey Alice!", False)
        assert out == "Hey Alice!"

    def test_json_output(self):
        out = format_success("Alice", "en", "casual", "Hey Alice!", True)
        data = json.loads(out)
        assert data["status"] == "success"
        assert data["data"]["name"] == "Alice"
        assert data["data"]["greeting"] == "Hey Alice!"


# ── format_error ─────────────────────────────────────────────────


class TestFormatError:
    def test_plain_text_error(self):
        out = format_error("INVALID_INPUT", "Name is empty", False)
        assert "INVALID_INPUT" in out
        assert "Name is empty" in out

    def test_json_error(self):
        out = format_error("INVALID_INPUT", "Name is empty", True)
        data = json.loads(out)
        assert data["status"] == "error"
        assert data["error"]["code"] == "INVALID_INPUT"


# ── run (end-to-end) ────────────────────────────────────────────


class TestRun:
    def test_success_returns_zero(self):
        out = io.StringIO()
        err = io.StringIO()
        code = run("Alice", "en", "casual", out_stream=out, err_stream=err)
        assert code == 0
        assert "Alice" in out.getvalue()
        assert err.getvalue() == ""

    def test_validation_error_returns_one(self):
        out = io.StringIO()
        err = io.StringIO()
        code = run("", "en", "casual", out_stream=out, err_stream=err)
        assert code == 1
        assert out.getvalue() == ""
        assert "Error" in err.getvalue()

    def test_json_success(self):
        out = io.StringIO()
        err = io.StringIO()
        code = run("Bob", "en", "formal", use_json=True, out_stream=out, err_stream=err)
        assert code == 0
        data = json.loads(out.getvalue())
        assert data["status"] == "success"

    def test_json_error(self):
        out = io.StringIO()
        err = io.StringIO()
        code = run("Bob", "xx", "formal", use_json=True, out_stream=out, err_stream=err)
        assert code == 1
        data = json.loads(err.getvalue())
        assert data["status"] == "error"

    def test_default_streams(self):
        """run() should default to sys.stdout / sys.stderr."""
        # Just ensure no TypeError when streams are omitted.
        # We don't capture output here — other tests cover that.
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            code = run("Test", "en", "casual")
            assert code == 0
        finally:
            sys.stdout = old_stdout
