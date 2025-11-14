import re
import sys
from time import sleep
from typing import Optional, Union

from dreamberd.builtin import KEYWORDS, Name, DreamberdValue, Variable
from dreamberd.processor.lexer import tokenize
from dreamberd.processor.syntax_tree import generate_syntax_tree
from dreamberd.interpreter import (
    interpret_code_statements_main_wrapper,
    load_global_dreamberd_variables,
    load_globals,
    load_public_global_variables,
)

__all__ = ["run_file"]

__REPL_FILENAME = "__repl__"
sys.setrecursionlimit(100000)


def run_file(main_filename: str) -> None:  # idk what else to call this

    with open(main_filename, "r", encoding="utf-8") as f:
        code_lines = f.readlines()

    # split up into seperate 'files' by finding which lines start with multiple equal signs
    files: list[tuple[Optional[str], str]] = []
    if any(matches := [re.match(r"=====.*", l) for l in code_lines]):
        for i, match in reversed([*enumerate(matches)]):
            if match is None:
                continue
            name = match.group().strip("=").strip() or None
            files.insert(0, (name, "".join(code_lines[i + 1 :])))
            del code_lines[i:]
        files.insert(0, (None, "".join(code_lines[0:])))
    else:
        files = [(None, "".join(code_lines))]

    # execute code for each file
    importable_names: dict[str, dict[str, DreamberdValue]] = {}
    for filename, code in files:
        filename = filename or "__unnamed_file__"
        # Set global variables for interpreter
        import dreamberd.interpreter as interpreter

        interpreter.filename = filename
        interpreter.code = code
        tokens = tokenize(filename, code)
        statements = generate_syntax_tree(filename, tokens, code)

        # load variables and run the code
        # Use Name objects directly for keywords
        namespaces: list[dict[str, Union[Variable, Name]]] = [KEYWORDS.copy()]  # type: ignore
        exported_names: list[tuple[str, str, DreamberdValue]] = []
        load_globals(
            filename,
            code,
            {},
            set(),
            exported_names,
            importable_names.get(filename, {}),
        )
        load_global_dreamberd_variables(namespaces)
        load_public_global_variables(namespaces)
        interpret_code_statements_main_wrapper(statements, namespaces, [], [{}])

        # take exported names and put them where they belong
        for target_filename, name, value in exported_names:
            if target_filename not in importable_names:
                importable_names[target_filename] = {}
            importable_names[target_filename][name] = value

    print(
        "\033[33mCode has finished executing. Press ^C once or twice to stop waiting for when-statements and after-statements.\033[039m",
        flush=True,
    )
    try:
        while True:
            sleep(1)  # just waiting for any clicks, when statements, etc
    except KeyboardInterrupt:
        exit()  # quit silently
