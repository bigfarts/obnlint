import argparse
import sys
import colorama
import collections

from luaparser import ast, astnodes, builder

from . import astutil

Lint = collections.namedtuple("Lint", ["source", "node", "message"])
Source = collections.namedtuple("Source", ["filename", "ast", "lines"])


def parse(f):
    raw = f.read().replace("\t", "    ")
    tree = ast.parse(raw)
    lines = raw.split("\n")
    return Source(f.name, tree, lines)


def log(tag: str, color: str, loc: str, message: str, context: str = None):
    print(
        f"{colorama.Style.BRIGHT}{loc}: {color}{tag}:{colorama.Fore.RESET} {message}{colorama.Style.RESET_ALL}"
    )
    if context is not None:
        print(context)


def log_lint(source: Source, node: astnodes.Node, message: str):
    start_line, start_col, end_line, end_col = astutil.get_node_range(node)

    log(
        "lint",
        colorama.Fore.CYAN,
        f"{source.filename}:{start_line}:{start_col}",
        message,
        "    "
        + source.lines[start_line - 1]
        + "\n"
        + "    "
        + " " * start_col
        + colorama.Fore.GREEN
        + "^"
        + "~"
        * (
            (end_col if start_line == end_line else len(source.lines[start_line - 1]))
            - start_col
            - 1
        )
        + colorama.Fore.RESET,
    )


def log_parse_error(filename: str, reason: str):
    log("error", colorama.Fore.RED, filename, reason)


def main():
    from .rules import RULES

    rules_by_name = {rule.rule_name: rule for rule in RULES}

    argparser = argparse.ArgumentParser(
        description="lint OBN scripts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="list of rules:\n\n"
        + "\n".join("  " + rule.rule_name + "\t" + rule.__doc__ for rule in RULES),
    )
    argparser.add_argument(
        "-W",
        action="append",
        metavar="RULE",
        help="enable/disable rules (use as -Wno-rule-name to disable a rule)",
        default=[],
    )
    argparser.add_argument("files", nargs="+", help="files to lint")

    args = argparser.parse_args()
    enabled_rules = [rule.rule_name for rule in RULES]
    for rule_name in args.W:
        if rule_name.startswith("no-"):
            enabled_rules.remove(rule_name[3:])
        else:
            enabled_rules.append(rule_name)

    for filename in args.files:
        with open(filename) as f:
            try:
                src = parse(f)
            except builder.SyntaxException as e:
                log_parse_error(filename, str(e))
                continue

        for rule_name in enabled_rules:
            rule = rules_by_name[rule_name]
            for lint in rule(src):
                log_lint(src, lint.node, lint.message + " [-W" + rule.rule_name + "]")
