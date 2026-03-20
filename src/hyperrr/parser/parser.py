import re
import textwrap

import yaml

from hyperrr.ast import PromptCallNode, TextNode, VariableNode
from hyperrr.exceptions import PromptParseError
from hyperrr.parser.args import parse_args

TOKEN_PATTERN = re.compile(r"\{\{\s*(.*?)\s*\}\}")


def parse(content: str):
    print("PARSING CONTENT:", content)

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

    # 🔥 support top-level expressions
    if not TOKEN_PATTERN.search(body):
        body = f"{{{{ {body} }}}}"

    nodes = []
    last_index = 0

    print("BODY:", body)

    for match in TOKEN_PATTERN.finditer(body):
        start, end = match.span()

        if start > last_index:
            nodes.append(TextNode(body[last_index:start]))

        expr = match.group(1).strip()

        print("EXPR:", expr)

        if expr.startswith("prompt("):
            ref, raw_kwargs = parse_args(expr)
            kwargs = {}

            for key, value in raw_kwargs.items():
                if isinstance(value, str) and "{{" in value:
                    _, nodes = parse(value)
                    kwargs[key] = nodes
                else:
                    kwargs[key] = value

            print("REF:", ref)

            nodes.append(
                PromptCallNode(
                    ref=ref,
                    kwargs=kwargs,
                )
            )
        else:
            nodes.append(VariableNode(expr))

        last_index = end

    if last_index < len(body):
        nodes.append(TextNode(body[last_index:]))

    return schema, nodes
