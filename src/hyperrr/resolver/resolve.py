from .file import FileResolver
from .registry import RegistryResolver

resolvers = [
    RegistryResolver(),
    FileResolver(),
]


def resolve(ref: str) -> str:
    print("RESOLVE:", ref)

    for resolver in resolvers:
        if resolver.can_resolve(ref):
            print("→ using", resolver.__class__.__name__)
            return resolver.resolve(ref)

    raise ValueError(f"No resolver found for {ref}")
