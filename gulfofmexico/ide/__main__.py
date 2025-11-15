from __future__ import annotations

import sys

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
    parser.add_argument(
        "--web",
        action="store_true",
        help="Force web-based IDE instead of Qt GUI.",
    )
    args = parser.parse_args()

    # Use web IDE if forced
    if args.web:
        print("Launching Web-based IDE...")
        from .web_ide import run_web_ide

        run_web_ide()
    else:
        # Try Qt GUI first
        try:
            from .app import run

            run(args.open or None, run_on_open=args.run)
        except Exception as exc:
            # Any error falls back to web IDE
            print(f"Qt GUI unavailable: {type(exc).__name__}")
            print("Launching Web-based IDE...")
            from .web_ide import run_web_ide

            run_web_ide()
