"""Greeter: a small, configurable command-line greeting tool."""

from .config import Config
from .core import (
    GreetingError,
    GreetingResult,
    build_greeting,
    greet,
)
from .config import VERSION as __version__

__all__ = [
    "Config",
    "GreetingError",
    "GreetingResult",
    "build_greeting",
    "greet",
    "__version__",
]
