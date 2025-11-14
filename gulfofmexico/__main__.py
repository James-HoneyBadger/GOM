"""Module entry-point.

Usage:
  python -m gulfofmexico               # Start REPL
  python -m gulfofmexico path/to.gom   # Run file
"""

from __future__ import annotations

import sys
from typing import List

from gulfofmexico import run_file
from gulfofmexico.repl import main as repl_main


def _main(argv: List[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        return repl_main([])
    if len(args) == 1:
        run_file(args[0])
        return 0
    print("Usage: python -m gulfofmexico [file.gom]")
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main())
