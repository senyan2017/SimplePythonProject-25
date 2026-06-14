"""Command-line entry point — thin wiring around app.greeting."""

import argparse
import sys

from app.greeting import format_greeting


def parse_args(argv=None):
    """Parse CLI arguments. Pass a list to make this testable."""
    parser = argparse.ArgumentParser(description="Print a friendly greeting.")
    parser.add_argument("--name", default=None, help="Name to greet.")
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="How many times to print the greeting.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Build the greeting(s) and print them. Returns the process exit code."""
    args = parse_args([] if argv is None else argv)
    line = format_greeting(name=args.name)
    print("\n".join(line for _ in range(args.repeat)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
