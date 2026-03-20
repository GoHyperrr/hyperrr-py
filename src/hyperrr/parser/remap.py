def remap_nodes(nodes, kwargs):
    return nodes
    # remapped = []

    # for node in nodes:
    #     if isinstance(node, TextNode):
    #         remapped.append(node)

    #     elif isinstance(node, VariableNode):
    #         if node.name in kwargs:
    #             value = kwargs[node.name].strip()

    #             if value.isidentifier():
    #                 remapped.append(VariableNode(name=value))
    #             else:
    #                 remapped.append(TextNode(text=value))
    #         else:
    #             remapped.append(node)

    # return remapped
