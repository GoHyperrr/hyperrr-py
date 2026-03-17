from hyperrr.exceptions import PromptResolutionError
from hyperrr.resolver.file import FileResolver
from hyperrr.resolver.inline import InlineResolver

# from hyperrr.resolver.registry import RegistryResolver


RESOLVERS = [
    FileResolver(),
    # RegistryResolver(),  # enable later
    InlineResolver(),  # ALWAYS last
]


def resolve(ref: str) -> str:
    for resolver in RESOLVERS:
        if resolver.can_resolve(ref):
            return resolver.resolve(ref)

    raise PromptResolutionError(f"Cannot resolve ref: {ref}")
