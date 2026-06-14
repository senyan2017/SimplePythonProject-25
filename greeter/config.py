"""Configuration handling for the greeter CLI.

Resolution order (highest priority first):

1. Values explicitly passed on the command line.
2. Environment variables (``GREETER_NAME`` / ``GREETER_LANGUAGE`` /
   ``GREETER_SCENE``).
3. Built-in defaults defined in this module.

Keeping this logic in one small, dependency-free module makes the precedence
rules easy to read and easy to unit test.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping, Optional

# Project version, surfaced through ``--version`` and ``greeter.__version__``.
VERSION = "1.0.0"

# Built-in defaults used when neither the CLI nor the environment provides a
# value.
DEFAULT_NAME = "World"
DEFAULT_LANGUAGE = "en"
DEFAULT_SCENE = "default"

# Environment variable names checked when a value is not given on the CLI.
ENV_NAME = "GREETER_NAME"
ENV_LANGUAGE = "GREETER_LANGUAGE"
ENV_SCENE = "GREETER_SCENE"


@dataclass
class Config:
    """Resolved settings used to build a greeting."""

    name: str = DEFAULT_NAME
    language: str = DEFAULT_LANGUAGE
    scene: str = DEFAULT_SCENE

    @classmethod
    def from_env(cls, env: Optional[Mapping[str, str]] = None) -> "Config":
        """Build a config from environment variables, falling back to defaults.

        ``env`` defaults to ``os.environ`` but can be injected in tests so we do
        not have to mutate global process state.
        """

        source = os.environ if env is None else env
        return cls(
            name=source.get(ENV_NAME, DEFAULT_NAME),
            language=source.get(ENV_LANGUAGE, DEFAULT_LANGUAGE),
            scene=source.get(ENV_SCENE, DEFAULT_SCENE),
        )

    @classmethod
    def resolve(
        cls,
        name: Optional[str] = None,
        language: Optional[str] = None,
        scene: Optional[str] = None,
        env: Optional[Mapping[str, str]] = None,
    ) -> "Config":
        """Combine CLI arguments, environment variables and defaults.

        Any argument left as ``None`` is treated as "not provided on the CLI"
        and therefore falls back to the environment / default layers.
        """

        resolved = cls.from_env(env)
        if name is not None:
            resolved.name = name
        if language is not None:
            resolved.language = language
        if scene is not None:
            resolved.scene = scene
        return resolved
