"""Module entry point for Gulf of Mexico.

Usage:
  - REPL (default):
      python -m gulfofmexico
  - Run a file:
      python -m gulfofmexico <file.gom>
  - Inline code:
      python -m gulfofmexico -c "print(123)!"
  - Show Python traceback on unhandled exceptions:
      python -m gulfofmexico -s <file.gom>

This uses the production interpreter path in gulfofmexico/interpreter.py.
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from gulfofmexico import run_file
from gulfofmexico.repl import main as repl_main


def _run_inline(code: str, show_tb: bool) -> int:
    # Execute inline code via the production interpreter path
    import gulfofmexico.interpreter as interpreter
    from gulfofmexico.processor.lexer import tokenize
    from gulfofmexico.processor.syntax_tree import generate_syntax_tree
    from gulfofmexico.builtin import KEYWORDS, Name, GulfOfMexicoValue, Variable
    from typing import Union

    try:
        filename = "__inline__"
        interpreter.filename = filename
        interpreter.code = code

        tokens = tokenize(filename, code)
        statements = generate_syntax_tree(filename, tokens, code)

        namespaces: list[dict[str, Union[Variable, Name]]] = [KEYWORDS.copy()]  # type: ignore
        exported_names: list[tuple[str, str, GulfOfMexicoValue]] = []
        importable_names: dict[str, dict[str, GulfOfMexicoValue]] = {}

        interpreter.load_globals(
            filename,
            code,
            {},
            set(),
            exported_names,
            importable_names.get(filename, {}),
        )
        interpreter.load_global_gulfofmexico_variables(namespaces)
        interpreter.load_public_global_variables(namespaces)

        interpreter.interpret_code_statements_main_wrapper(
            statements,
            namespaces,
            [],
            [{}],
            importable_names,
            exported_names,
        )
        return 0
    except Exception:
        if show_tb:
            raise
        print("Error during execution.", file=sys.stderr)
        return 1


def _main(argv: Optional[list[str]] = None) -> int:
    args = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(prog="gulfofmexico", add_help=True)
    parser.add_argument("file", nargs="?", help="Gulf of Mexico source file (.gom)")
    parser.add_argument(
        "-s",
        "--show-traceback",
        action="store_true",
        help="show full Python traceback on errors",
    )
    parser.add_argument("-c", dest="inline_code", help="run inline code and exit")
    ns = parser.parse_args(args)

    # Inline code mode
    if ns.inline_code is not None:
        try:
            return _run_inline(ns.inline_code, ns.show_traceback)
        except Exception:
            if ns.show_traceback:
                raise
            return 1

    # File mode
    if ns.file:
        try:
            run_file(ns.file)
            return 0
        except Exception:
            if ns.show_traceback:
                raise
            return 1

    # Default: REPL
    try:
        return repl_main([])
    except Exception:
        if ns.show_traceback:
            raise
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main())
