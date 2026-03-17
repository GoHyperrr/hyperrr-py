import os

from hyperrr.exceptions import PromptResolutionError


def resolve(ref: str) -> str:
    # file
    if os.path.isfile(ref):
        try:
            with open(ref, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise PromptResolutionError(f"Failed to read {ref}: {e}")

    # inline fallback
    return ref
