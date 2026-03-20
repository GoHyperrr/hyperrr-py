from hyperrr.ast import PromptCallNode, TextNode, VariableNode
from hyperrr.parser.parser import parse
from hyperrr.resolver.resolve import resolve
from hyperrr.validator.validator import validate


def execute(nodes, inputs):
    output = ""

    for node in nodes:
        if isinstance(node, TextNode):
            output += node.text

        elif isinstance(node, VariableNode):
            output += str(inputs.get(node.name, ""))

        elif isinstance(node, PromptCallNode):
            # 🔥 resolve kwargs (nested AST support)
            resolved_kwargs = {}

            for key, value in node.kwargs.items():
                if isinstance(value, list):
                    resolved_kwargs[key] = execute(value, inputs)
                else:
                    resolved_kwargs[key] = value

            # 🔥 fetch prompt
            raw = resolve(node.ref)

            # 🔥 parse fetched prompt
            schema, child_nodes = parse(raw)

            # 🔥 merge parent inputs + kwargs
            merged_inputs = {
                **inputs,  # parent inputs
                **resolved_kwargs,  # explicit overrides
            }

            print("Merged inputs for prompt call:", merged_inputs)

            # validate against merged inputs
            validate(schema, merged_inputs)

            # recursive execution
            output += execute(child_nodes, merged_inputs)

            print("Output after executing prompt call:", output)

    return output
