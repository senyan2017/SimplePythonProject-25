"""CLI argument parsing."""

import argparse

from greeter.core import SUPPORTED_LANGS, SUPPORTED_SCENES


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for the greeter CLI."""
    parser = argparse.ArgumentParser(
        prog="greeter",
        description="A lightweight CLI greeting tool with multi-language and scene support.",
    )

    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default=None,
        help="Name of the person to greet (default: env GREETER_NAME or 'World')",
    )

    parser.add_argument(
        "-l",
        "--lang",
        type=str,
        default=None,
        choices=list(SUPPORTED_LANGS),
        help="Greeting language (default: env GREETER_LANG or 'en')",
    )

    parser.add_argument(
        "-s",
        "--scene",
        type=str,
        default=None,
        choices=list(SUPPORTED_SCENES),
        help="Greeting scene/style (default: env GREETER_SCENE or 'casual')",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        default=None,
        dest="json",
        help="Output result as JSON (default: env GREETER_JSON or plain text)",
    )

    return parser


def parse_args(argv=None) -> dict:
    """Parse CLI arguments and return as a dict.

    Args:
        argv: argument list (defaults to sys.argv[1:])

    Returns:
        dict with keys: name, lang, scene, json
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    return vars(args)
