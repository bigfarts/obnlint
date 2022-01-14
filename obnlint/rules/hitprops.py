from .. import astutil, Lint, Source

from luaparser import ast, astnodes


def check_hitprops_damage(source: Source):
    """Checks if HitProps.new uses damage from CardProperties."""
    for node in ast.walk(source.ast):
        if astutil.node_partially_matches(
            node,
            astnodes.Call(
                func=astnodes.Index(
                    value=astnodes.Name("HitProps"), idx=astnodes.Name("new")
                ),
                args=[None, None, None, None, None],
            ),
        ):
            if not astutil.node_partially_matches_anywhere(
                node.args[0],
                astnodes.Index(value=None, idx=astnodes.Name("damage")),
            ):  # Damage
                if check_hitprops_damage.rule_name in astutil.get_nolint_advice(
                    source, node.args[0]
                ):
                    continue

                yield Lint(
                    source,
                    node.args[0],
                    "HitProps.new does not appear to use CardProperties.damage for hit damage",
                )


check_hitprops_damage.rule_name = "hitprops-damage"


def check_hitprops_element(source: Source):
    """Checks if HitProps.new uses element from CardProperties."""
    for node in ast.walk(source.ast):
        if astutil.node_partially_matches(
            node,
            astnodes.Call(
                func=astnodes.Index(
                    value=astnodes.Name("HitProps"), idx=astnodes.Name("new")
                ),
                args=[None, None, None, None, None],
            ),
        ):
            if not astutil.node_partially_matches_anywhere(
                node.args[2],
                astnodes.Index(value=None, idx=astnodes.Name("element")),
            ):  # Element
                if check_hitprops_element.rule_name in astutil.get_nolint_advice(
                    source, node.args[2]
                ):
                    continue

                yield Lint(
                    source,
                    node.args[2],
                    "HitProps.new does not appear to use CardProperties.element for hit element",
                )


check_hitprops_element.rule_name = "hitprops-element"


def check_hitprops_flags(source: Source):
    """Checks if HitProps.new uses flags from CardProperties."""
    for node in ast.walk(source.ast):
        if astutil.node_partially_matches(
            node,
            astnodes.Call(
                func=astnodes.Index(
                    value=astnodes.Name("HitProps"), idx=astnodes.Name("new")
                ),
                args=[None, None, None, None, None],
            ),
        ):
            if not astutil.node_partially_matches_anywhere(
                node.args[1],
                astnodes.Index(value=None, idx=astnodes.Name("hit_flags")),
            ):  # Flags
                if check_hitprops_flags.rule_name in astutil.get_nolint_advice(
                    source, node.args[1]
                ):
                    continue

                yield Lint(
                    source,
                    node.args[2],
                    "HitProps.new does not appear to use CardProperties.hit_flags for hit flags",
                )


check_hitprops_flags.rule_name = "hitprops-flags"

RULES = [check_hitprops_damage, check_hitprops_element, check_hitprops_flags]
