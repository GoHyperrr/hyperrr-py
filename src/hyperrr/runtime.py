from hyperrr.executor.executor import execute
from hyperrr.parser.parser import parse
from hyperrr.validator.validator import validate


def prompt(ref: str, **inputs):

    schema, nodes = parse(ref)

    print("Parsed schema:", schema)

    validate(schema, inputs)

    return execute(nodes, inputs)
