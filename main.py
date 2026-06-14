"""Thin entry point for the greeter CLI.

All real logic lives in the :mod:`greeter` package so it stays importable and
testable; this file just wires the package's ``main`` to the process exit code.
"""

import sys

from greeter.cli import main

if __name__ == "__main__":
    sys.exit(main())
