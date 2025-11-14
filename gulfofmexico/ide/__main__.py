from __future__ import annotations

import sys

try:
    from .app import run
except ImportError as exc:  # pragma: no cover - surface clear message
    msg = (
        "Unable to start GUI IDE. "
        "Ensure PySide6 is installed (pip install PySide6) or install the "
        "optional Poetry extra: poetry install -E ide.\n"
        f"Details: {exc}"
    )
    print(msg)
    sys.exit(1)
else:
    if __name__ == "__main__":
        import argparse

        parser = argparse.ArgumentParser(description="Gulf of Mexico IDE")
        parser.add_argument(
            "-o",
            "--open",
            action="append",
            help="Open a file on startup. Can be given multiple times.",
        )
        parser.add_argument(
            "--run",
            action="store_true",
            help="Run the active editor after opening files.",
        )
        args = parser.parse_args()

        try:
            run(args.open or None, run_on_open=args.run)
        except RuntimeError as exc:  # pragma: no cover
            print(str(exc))
            sys.exit(1)
