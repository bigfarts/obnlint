from luaparser import ast, astnodes


def node_partially_matches(node: astnodes.Node, pattern: astnodes.Node) -> bool:
    if pattern is None:
        return True

    if type(node) != type(pattern):
        return False

    if isinstance(pattern, astnodes.Node):
        for k, v in pattern.__dict__.items():
            if k[0] == "_":
                continue
            if not node_partially_matches(getattr(node, k), v):
                return False
        return True
    elif isinstance(pattern, list):
        return all(node_partially_matches(x, y) for x, y in zip(node, pattern))

    return node == pattern


def node_partially_matches_anywhere(
    node: astnodes.Node, pattern: astnodes.Node
) -> bool:
    for c in ast.walk(node):
        if node_partially_matches(c, pattern):
            return True
    return False


def get_node_range(node: astnodes.Node):
    start_line = 0
    start_col = 0
    end_line = 0
    end_col = 0

    for c in ast.walk(node):
        if c.first_token is None:
            continue

        if start_line == 0:
            start_line = c.line
            start_col = c.first_token.column

        if c.line > end_line:
            end_line = c.line
            end_col = 0

        if c.last_token.column + len(c.last_token.text) > end_col:
            end_col = c.last_token.column + len(c.last_token.text)

    return start_line, start_col, end_line, end_col


def get_nolint_advice(source, node: astnodes.Node):
    advice = set()

    line_ends = {}
    for c in ast.walk(node):
        if c.first_token is None:
            continue

        if c.line not in line_ends:
            line_ends[c.line] = 0
        end_col = c.last_token.column + len(c.last_token.text)
        if end_col > line_ends[c.line]:
            line_ends[c.line] = end_col

    for lineno, colno in line_ends.items():
        _, _, tail = source.lines[lineno - 1][colno:].partition("--")
        if not tail:
            continue
        tail = tail.strip()
        if not tail.startswith("NOLINT:"):
            continue

        tail = tail[len("NOLINT:") :].strip()

        advice.update(p.strip() for p in tail.split(","))

    return advice
