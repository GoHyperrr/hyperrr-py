import os

from hyperrr.exceptions import PromptResolutionError
from hyperrr.resolver.base import Resolver


class FileResolver(Resolver):
    def can_resolve(self, ref: str) -> bool:
        return os.path.isfile(ref)

    def resolve(self, ref: str) -> str:
        try:
            with open(ref, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise PromptResolutionError(f"Failed to read file {ref}: {e}")
