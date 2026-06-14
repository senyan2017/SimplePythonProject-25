"""Command-line interface for the greeter tool.

The parser stays intentionally small: three optional value flags plus
``--version``. Domain validation lives in :mod:`greeter.core`, so invalid
languages/scenes flow through to the structured result instead of being rejected
by argparse -- this keeps error reporting consistent and testable.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .config import VERSION, Config
from .core import SUPPORTED_LANGUAGES, SUPPORTED_SCENES, greet


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the greeter CLI."""

    parser = argparse.ArgumentParser(
        prog="greeter",
        description="Print a configurable greeting.",
        epilog=(
            "If a flag is omitted, the value falls back to the matching "
            "environment variable (GREETER_NAME / GREETER_LANGUAGE / "
            "GREETER_SCENE) and finally to a built-in default."
        ),
    )
    parser.add_argument(
        "-n",
        "--name",
        default=None,
        help="who to greet (default: env GREETER_NAME or 'World')",
    )
    parser.add_argument(
        "-l",
        "--language",
        default=None,
        help="greeting language: {} (default: env GREETER_LANGUAGE or 'en')".format(
            ", ".join(SUPPORTED_LANGUAGES)
        ),
    )
    parser.add_argument(
        "-s",
        "--scene",
        default=None,
        help="greeting scene: {} (default: env GREETER_SCENE or 'default')".format(
            ", ".join(SUPPORTED_SCENES)
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {}".format(VERSION),
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point: parse args, build the greeting and print the outcome.

    Returns the process exit code: ``0`` on success, ``2`` on a validation
    failure. Successful greetings go to stdout; errors go to stderr so the two
    can be told apart when running inside a container.
    """

    parser = build_parser()
    args = parser.parse_args(argv)

    config = Config.resolve(name=args.name, language=args.language, scene=args.scene)
    result = greet(config)

    if result.ok:
        print(result.message)
    else:
        print(
            "error: {} (code={})".format(result.message, result.code),
            file=sys.stderr,
        )
    return result.exit_code
