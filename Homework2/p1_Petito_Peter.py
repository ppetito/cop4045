# Peter Petito - Homework 2
# Problem 1
import ast
import io
import tokenize
from typing import Tuple


def line_number(source_filename: str, target_filename: str) -> None:
    """Write each line of source_filename to target_filename, prefixed with its line number"""
    try:
        with open(source_filename, 'r') as infile:
            lines = infile.readlines()
        with open(target_filename, 'w') as outfile:
            for i, line in enumerate(lines, start=1):
                outfile.write(f"{i}. {line}")
                if not line.endswith('\n'):
                    outfile.write('\n')
    except Exception as error:
        print(f"Error numbering lines from '{source_filename}' to '{target_filename}': {error}")
        raise


def _strip_comments_and_blanks(code: str) -> str:
    lines = code.split('\n')
    try:
        for tok in tokenize.generate_tokens(io.StringIO(code).readline):
            if tok.type == tokenize.COMMENT:
                row, col = tok.start
                lines[row - 1] = lines[row - 1][:col].rstrip()
    except tokenize.TokenizeError:
        pass
    lines = [ln for ln in lines if ln.strip()]
    return '\n'.join(lines) + '\n' if lines else ''


def _args_string(node: ast.FunctionDef) -> str:
    a = node.args
    parts = [x.arg for x in getattr(a, 'posonlyargs', [])] + [x.arg for x in a.args]
    if a.vararg:
        parts.append('*' + a.vararg.arg)
    parts += [x.arg for x in a.kwonlyargs]
    if a.kwarg:
        parts.append('**' + a.kwarg.arg)
    return ', '.join(parts)


def parse_functions(filename: str) -> Tuple[Tuple[int, str, str, str], ...]:
    """Return (line_no, name, args, code) for each top level function in filename, sorted by name."""
    try:
        with open(filename, 'r') as f:
            source = f.read()
        tree = ast.parse(source, filename=filename)
        src_lines = source.split('\n')
        functions = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                end = getattr(node, 'end_lineno', node.lineno)
                raw = '\n'.join(src_lines[node.lineno - 1:end]) + '\n'
                functions.append((node.lineno, node.name, _args_string(node), _strip_comments_and_blanks(raw)))
        functions.sort(key=lambda t: t[1])
        return tuple(functions)
    except Exception as error:
        print(f"Error parsing '{filename}': {error}")
        raise


def main() -> None:
    this_file = __file__
    out_file = "p1_line_numbers_output.txt"
    line_number(this_file, out_file)
    print(f"Part a): numbered lines written to '{out_file}'.\n")

    print("Part b): functions (sorted alphabetically by name):")
    for func in parse_functions(this_file):
        print(func)


if __name__ == "__main__":
    main()