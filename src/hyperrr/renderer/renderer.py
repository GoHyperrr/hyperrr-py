from hyperrr.ast import TextNode, VariableNode


def render(nodes, inputs):
    output = []
    print("Rendering with inputs:", inputs)
    print("Nodes:", nodes)
    for node in nodes:
        if isinstance(node, TextNode):
            output.append(node.text)

        elif isinstance(node, VariableNode):
            if node.name not in inputs:
                raise Exception(f"Missing variable: {node.name}")

            output.append(str(inputs[node.name]))

    return "".join(output)
