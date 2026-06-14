"""Greeter CLI entry point."""

import sys

from greeter.cli import parse_args
from greeter.config import load_config
from greeter.core import run


def main() -> int:
    cli_args = parse_args()
    config = load_config(cli_args)

    exit_code = run(
        name=config["name"],
        lang=config["lang"],
        scene=config["scene"],
        use_json=config["json"],
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
