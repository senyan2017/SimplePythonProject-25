import argparse
import sys


def greet(name=None):
    """Return a greeting string for the given name."""
    if name is None:
        return "Let's Python Project"

    name = name.strip()
    if not name:
        raise ValueError("Name must not be empty")
    if not all(c.isprintable() for c in name):
        raise ValueError("Name contains invalid characters")

    return f"Hello, {name}! Welcome to Let's Python Project"


def main():
    parser = argparse.ArgumentParser(
        description="A simple greeting program for Let's Python Project"
    )
    parser.add_argument(
        "--name", "-n",
        type=str,
        default=None,
        help="Name to greet (optional; prints default message if omitted)",
    )
    args = parser.parse_args()

    try:
        print(greet(args.name))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
