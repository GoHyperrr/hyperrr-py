from hyperrr.parser.parser import parse
from hyperrr.renderer.renderer import render
from hyperrr.resolver.resolve import resolve
from hyperrr.validator.validator import validate


def prompt(ref: str, **inputs):
    raw = resolve(ref)

    schema, nodes = parse(raw)
    print("Parsed schema:", schema)
    validate(schema, inputs)

    return render(nodes, inputs)
