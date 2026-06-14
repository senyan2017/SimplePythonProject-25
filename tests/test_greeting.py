"""Tests for app.config and app.greeting — default output & parameter combos."""

from app.config import PROJECT_NAME
from app.greeting import format_greeting


class TestConfig:
    def test_project_name_is_set(self):
        assert PROJECT_NAME == "Las's Python Project"

    def test_project_name_is_string(self):
        assert isinstance(PROJECT_NAME, str)


class TestGreetingDefault:
    def test_default_output(self):
        """No arguments → plain welcome with project name."""
        assert format_greeting() == "Welcome to Las's Python Project"

    def test_default_no_name_substring(self):
        result = format_greeting()
        assert "Hello" not in result


class TestGreetingWithParams:
    def test_with_name(self):
        result = format_greeting(name="Alice")
        assert result == "Hello, Alice! Welcome to Las's Python Project"

    def test_with_custom_project(self):
        result = format_greeting(project_name="My App")
        assert result == "Welcome to My App"

    def test_with_name_and_project(self):
        result = format_greeting(name="Bob", project_name="TestProj")
        assert result == "Hello, Bob! Welcome to TestProj"

    def test_returns_string(self):
        assert isinstance(format_greeting(), str)
        assert isinstance(format_greeting(name="X"), str)
