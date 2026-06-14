"""Tests for greeting construction, validation and structured results."""

import pytest

from greeter.config import Config
from greeter.core import (
    EXIT_OK,
    EXIT_VALIDATION,
    MAX_NAME_LENGTH,
    SUPPORTED_LANGUAGES,
    SUPPORTED_SCENES,
    GreetingError,
    GreetingResult,
    build_greeting,
    greet,
)


def test_build_greeting_default_english():
    assert build_greeting("World", "en", "default") == "Hello, World!"


def test_build_greeting_korean_morning():
    assert build_greeting("Bob", "ko", "morning") == "좋은 아침이에요, Bob!"


@pytest.mark.parametrize("language", SUPPORTED_LANGUAGES)
def test_build_greeting_all_languages_default(language):
    assert build_greeting("X", language, "default").endswith(", X!")


@pytest.mark.parametrize("scene", SUPPORTED_SCENES)
def test_build_greeting_all_scenes(scene):
    assert build_greeting("X", "en", scene).endswith(", X!")


def test_build_greeting_strips_name():
    assert build_greeting("  Bob  ", "en", "default") == "Hello, Bob!"


def test_empty_name_raises():
    with pytest.raises(GreetingError) as exc:
        build_greeting("   ", "en", "default")
    assert exc.value.code == "EMPTY_NAME"


def test_long_name_raises():
    with pytest.raises(GreetingError) as exc:
        build_greeting("a" * (MAX_NAME_LENGTH + 1), "en", "default")
    assert exc.value.code == "NAME_TOO_LONG"


def test_unsupported_language_raises():
    with pytest.raises(GreetingError) as exc:
        build_greeting("Bob", "xx", "default")
    assert exc.value.code == "UNSUPPORTED_LANGUAGE"


def test_unsupported_scene_raises():
    with pytest.raises(GreetingError) as exc:
        build_greeting("Bob", "en", "party")
    assert exc.value.code == "UNSUPPORTED_SCENE"


def test_greet_success_returns_result():
    res = greet(Config(name="Bob", language="en", scene="default"))
    assert isinstance(res, GreetingResult)
    assert res.ok is True
    assert res.message == "Hello, Bob!"
    assert res.code == "OK"
    assert res.exit_code == EXIT_OK


def test_greet_failure_returns_result():
    res = greet(Config(name="", language="en", scene="default"))
    assert res.ok is False
    assert res.code == "EMPTY_NAME"
    assert res.exit_code == EXIT_VALIDATION


def test_greet_unsupported_language_failure():
    res = greet(Config(name="Bob", language="xx", scene="default"))
    assert res.ok is False
    assert res.code == "UNSUPPORTED_LANGUAGE"
