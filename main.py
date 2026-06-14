"""Minimal example CLI for GSM students.

Default behaviour
    Running with no arguments prints the project banner: "Let's Python Project".

Optional greeting
    Passing --name/-n NAME prints a personalised greeting. Surrounding
    whitespace on the name is trimmed before use.

Error handling (input is never silently swallowed)
    * empty or whitespace-only name -> ValueError ("must not be empty")
    * name with non-printable / control characters -> ValueError
      ("invalid characters")
    The CLI turns these into a clear "Error: ..." message on stderr and exits
    with a non-zero status, so local runs and container runs fail loudly and
    in exactly the same way.
"""

from __future__ import annotations

import argparse
import sys

BANNER = "Let's Python Project"


def greet(name: str | None = None) -> str:
    """Return the greeting text.

    With no name (the default) the project banner is returned unchanged.
    With a name, a personalised greeting is returned after trimming whitespace.

    Raises:
        ValueError: if ``name`` is given but is empty/whitespace-only, or
            contains non-printable characters.
    """
    if name is None:
        return BANNER

    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name must not be empty")
    if not cleaned.isprintable():
        raise ValueError("name contains invalid characters")
    return f"Hello, {cleaned}! Welcome to {BANNER}"


def _force_utf8(stream) -> None:
    """Best-effort: reconfigure a text stream to UTF-8.

    Keeps output identical regardless of the host/container locale. It is a
    no-op on streams that do not support reconfiguration.
    """
    reconfigure = getattr(stream, "reconfigure", None)
    if reconfigure is not None:
        try:
            reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Print a greeting. Same behaviour locally and in Docker.",
    )
    parser.add_argument(
        "-n",
        "--name",
        default=None,
        help="optional name to greet; omit to print the default banner",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns the process exit code (0 = success)."""
    _force_utf8(sys.stdout)
    _force_utf8(sys.stderr)

    parser = build_parser()
    args = parser.parse_args(argv)  # unknown flags -> argparse exits with code 2

    try:
        message = greet(args.name)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
