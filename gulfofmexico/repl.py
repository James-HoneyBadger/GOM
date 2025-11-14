"""
Interactive REPL for the Gulf of Mexico language (production interpreter).

Features:
- Real execution path: tokenize → generate_syntax_tree → interpret_code_statements_main_wrapper
- Persistent state across inputs (namespaces, watchers, globals)
- Multi-line input with automatic continuation until code parses
- Commands: :help, :quit, :reset, :load <file>, :vars

This REPL intentionally avoids the experimental engine; it uses the
monolithic production interpreter in gulfofmexico/interpreter.py.
"""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Optional, Union

from gulfofmexico.builtin import KEYWORDS, Name, GulfOfMexicoValue, Variable
from gulfofmexico.processor.lexer import tokenize
from gulfofmexico.processor.syntax_tree import generate_syntax_tree
from gulfofmexico.base import InterpretationError
import gulfofmexico.interpreter as interpreter


PRIMARY_PROMPT = "gom> "
CONT_PROMPT = " ...> "
REPL_FILENAME = "__repl__"


class GomRepl:
    """Stateful REPL runner bound to the production interpreter."""

    def __init__(self) -> None:
        # Shared state across inputs
        # Namespaces: first element is a copy of keyword namespace
        self.namespaces: list[dict[str, Union[Variable, Name]]] = [
            KEYWORDS.copy()  # type: ignore
        ]
        # When/after support with proper types from interpreter
        self.async_statements: interpreter.AsyncStatements = []
        self.when_statement_watchers: interpreter.WhenStatementWatchers = [{}]
        # Export/import map across pseudo-files
        self.importable_names: dict[str, dict[str, GulfOfMexicoValue]] = {}

        # Basic interpreter environment setup
        sys.setrecursionlimit(100000)

        # Load global, public, and runtime globals into namespaces
        # We use an empty code block for initialization
        interpreter.filename = REPL_FILENAME
        interpreter.code = ""
        exported_names: list[tuple[str, str, GulfOfMexicoValue]] = []
        interpreter.load_globals(
            interpreter.filename,
            interpreter.code,
            {},
            set(),
            exported_names,
            self.importable_names.get(interpreter.filename, {}),
        )
        interpreter.load_global_gulfofmexico_variables(self.namespaces)
        interpreter.load_public_global_variables(self.namespaces)

    def banner(self) -> str:
        return (
            "Gulf of Mexico REPL (production interpreter)\n"
            "Type :help for commands, :quit to exit."
        )

    def _read_multiline(self) -> Optional[str]:
        """
        Read one logical code block, allowing multi-line input until it parses.
        Returns None on EOF (Ctrl-D).
        """
        lines: list[str] = []
        prompt = PRIMARY_PROMPT
        while True:
            try:
                line = input(prompt)
            except EOFError:
                return None
            # Meta-commands handled only when first and as a single block
            if not lines and line.strip().startswith(":"):
                return line.strip()

            lines.append(line)
            candidate = "\n".join(lines)

            # Try parsing to determine completeness
            try:
                interpreter.filename = REPL_FILENAME
                interpreter.code = candidate
                tokens = tokenize(interpreter.filename, candidate)
                _ = generate_syntax_tree(
                    interpreter.filename, tokens, candidate
                )
                # If parse succeeds, return buffer
                return candidate
            except InterpretationError as e:
                # Heuristic: if likely incomplete input, continue
                # Check for common trailing characters or unmatched braces
                open_braces = candidate.count("{") - candidate.count("}")
                ends_with_open = candidate.rstrip().endswith(("{", ",", ":"))
                missing_punct = not candidate.rstrip().endswith(
                    ("!", "?", "}", ")", "]")
                )
                if open_braces > 0 or ends_with_open or missing_punct:
                    prompt = CONT_PROMPT
                    continue
                # Otherwise, show error and reset buffer
                print(f"\x1b[31m{e}\x1b[0m")
                return ""

    def _cmd_help(self) -> None:
        print(
            "\n".join(
                [
                    ":help              Show this help",
                    ":quit | :q         Exit the REPL",
                    ":reset             Reset all REPL state",
                    ":load <file>       Load and execute a .gom file",
                    ":vars              List current variables",
                ]
            )
        )

    def _cmd_reset(self) -> None:
        self.namespaces = [KEYWORDS.copy()]  # type: ignore
        self.async_statements = []
        self.when_statement_watchers = [{}]
        self.importable_names.clear()
        print("State reset.")

    def _cmd_vars(self) -> None:
        top = self.namespaces[-1] if self.namespaces else {}
        vars_only = {k: v for k, v in top.items() if isinstance(v, Variable)}
        if not vars_only:
            print("<no variables>")
            return
        for k, v in vars_only.items():
            # Variable may wrap a value; best-effort display
            current = v.value.value if hasattr(v.value, "value") else v.value
            print(f"{k} = {current}")

    def _cmd_load(self, path: str) -> None:
        file = Path(path).expanduser()
        if not file.exists():
            print(f"No such file: {file}")
            return
        try:
            code = file.read_text(encoding="utf-8")
        except OSError as e:
            print(f"Failed to read {file}: {e}")
            return
        self._execute(code, filename=str(file))

    def _dispatch_command(self, cmd: str) -> bool:
        """
        Handle meta-commands. Return True to continue, False to quit.
        """
        parts = cmd.split()
        if not parts:
            return True
        op = parts[0]
        if op in (":quit", ":q"):
            return False
        if op == ":help":
            self._cmd_help()
            return True
        if op == ":reset":
            self._cmd_reset()
            return True
        if op == ":vars":
            self._cmd_vars()
            return True
        if op == ":load":
            if len(parts) < 2:
                print("Usage: :load <file>")
                return True
            self._cmd_load(" ".join(parts[1:]))
            return True
        print(f"Unknown command: {op}. Try :help")
        return True

    def _execute(self, code: str, *, filename: Optional[str] = None) -> None:
        if code.strip() == "":
            return
        fname = filename or REPL_FILENAME
        exported_names: list[tuple[str, str, GulfOfMexicoValue]] = []

        # Prepare interpreter module state
        interpreter.filename = fname
        interpreter.code = code

        tokens = tokenize(fname, code)
        statements = generate_syntax_tree(fname, tokens, code)

        # Execute
        try:
            result = interpreter.interpret_code_statements_main_wrapper(
                statements,
                self.namespaces,  # preserve across inputs
                self.async_statements,
                self.when_statement_watchers,
                self.importable_names,
                exported_names,
            )
        except InterpretationError as e:
            print(f"\x1b[31m{e}\x1b[0m")
            return

        # Handle exported names
        for target_filename, name, value in exported_names:
            if target_filename not in self.importable_names:
                self.importable_names[target_filename] = {}
            self.importable_names[target_filename][name] = value

        if result is not None:
            # Best-effort print of result
            print(result)

    def loop(self) -> None:
        print(self.banner())
        while True:
            block = self._read_multiline()
            if block is None:
                # EOF
                print()
                return
            if block.startswith(":"):
                if not self._dispatch_command(block):
                    return
                continue
            self._execute(block)


def main(argv: list[str] | None = None) -> int:
    _ = argv or sys.argv[1:]
    repl = GomRepl()
    repl.loop()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
