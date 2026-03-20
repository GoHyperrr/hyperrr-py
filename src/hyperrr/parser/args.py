import ast


def parse_args(expr: str):
    tree = ast.parse(expr, mode="eval")
    call = tree.body

    if not isinstance(call, ast.Call):
        raise ValueError("Invalid function call")

    args = call.args
    kwargs = {}

    if not args:
        raise ValueError("prompt() requires ref")

    ref = ast.literal_eval(args[0])

    for kw in call.keywords:
        val = kw.value

        if isinstance(val, ast.Constant):
            kwargs[kw.arg] = val.value

        else:
            # 🔥 return raw python expression string
            kwargs[kw.arg] = ast.unparse(val)

    return ref, kwargs
