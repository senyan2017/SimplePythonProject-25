"""Greeting output logic — pure functions, easy to test."""

from app.config import PROJECT_NAME


def format_greeting(name=None, project_name=None):
    """Build a single greeting line. Returns a plain string, no side effects."""
    if project_name is None:
        project_name = PROJECT_NAME
    if name:
        return f"Hello, {name}! Welcome to {project_name}"
    return f"Welcome to {project_name}"
