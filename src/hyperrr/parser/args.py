def split_args(arg_string: str):
    parts = []
    current = ""
    in_string = False
    quote = None

    for c in arg_string:
        if c in ("'", '"'):
            if in_string and c == quote:
                in_string = False
            elif not in_string:
                in_string = True
                quote = c

        elif c == "," and not in_string:
            parts.append(current.strip())
            current = ""
            continue

        current += c

    if current:
        parts.append(current.strip())

    return parts


def parse_args(arg_string: str):
    parts = split_args(arg_string)

    ref = parts[0].strip().strip('"').strip("'")
    kwargs = {}

    for part in parts[1:]:
        key, value = part.split("=", 1)
        kwargs[key.strip()] = value.strip()

    return ref, kwargs


def resolve_value(value: str, context: dict):
    value = value.strip()

    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]

    if value in context:
        return context[value]

    return value
