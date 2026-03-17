def validate(schema, inputs):
    for key, spec in schema.items():
        required = True

        if isinstance(spec, str):
            required = not spec.endswith("?")

        if key not in inputs and required:
            raise Exception(f"Missing input: {key}")
