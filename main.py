#!/usr/bin/env python3
"""Project entry point."""

import argparse

from app.greeting import format_greeting


def parse_args(argv=None):
    """Parse command-line arguments. *argv* defaults to sys.argv[1:]."""
    parser = argparse.ArgumentParser(
        description="Las's Python Project",
    )
    parser.add_argument("--name", type=str, default=None, help="Name to greet")
    parser.add_argument(
        "--repeat", type=int, default=1, help="How many times to print (default: 1)"
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Run the application: parse args -> build output -> print."""
    args = parse_args(argv)
    for _ in range(args.repeat):
        print(format_greeting(name=args.name))


if __name__ == "__main__":
    main()
