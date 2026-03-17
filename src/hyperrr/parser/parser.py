import re
import textwrap

import yaml

from hyperrr.ast import TextNode, VariableNode
from hyperrr.exceptions import PromptParseError
from hyperrr.parser.args import parse_args
from hyperrr.parser.remap import remap_nodes
from hyperrr.resolver.resolve import resolve

TOKEN_PATTERN = re.compile(r"{{\s*(.*?)\s*}}")


def parse(content: str):
    content = content.strip()

    if content.startswith("---"):
        parts = content.split("---", 2)

        if len(parts) < 3:
            raise PromptParseError("Invalid frontmatter format")

        _, fm, body = parts

        fm = textwrap.dedent(fm).strip()
        body = textwrap.dedent(body).strip()

        meta = yaml.safe_load(fm) or {}
        schema = meta.get("inputs", {})
    else:
        body = textwrap.dedent(content).strip()
        schema = {}

    # 🔥 Build AST
    nodes = []
    last_index = 0

    for match in TOKEN_PATTERN.finditer(body):
        start, end = match.span()

        # text before
        if start > last_index:
            nodes.append(TextNode(body[last_index:start]))

        expr = match.group(1).strip()

        # 🔥 inline prompt() → resolve + inline AST
        if expr.startswith("prompt("):
            ref, kwargs = parse_args(expr[7:-1])

            raw = resolve(ref)
            child_schema, child_nodes = parse(raw)

            # remap variables
            remapped = remap_nodes(child_nodes, kwargs)

            nodes.extend(remapped)

        else:
            nodes.append(VariableNode(name=expr))

        last_index = end

    # remaining text
    if last_index < len(body):
        nodes.append(TextNode(body[last_index:]))

    return schema, nodes
