from hyperrr.resolver.base import Resolver


class InlineResolver(Resolver):
    def can_resolve(self, ref: str) -> bool:
        return True  # always fallback

    def resolve(self, ref: str) -> str:
        return ref
