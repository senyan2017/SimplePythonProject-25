"""Greeting output logic — pure functions, easy to test."""

from app.config import PROJECT_NAME


def format_greeting(name=None, project_name=None):
    """Build a single greeting line. Returns a plain string, no side effects."""
    label = project_name or PROJECT_NAME
    if name:
        return f"Hello, {name}! Welcome to {label}"
    return f"Welcome to {label}"
