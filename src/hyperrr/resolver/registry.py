from hyperrr.resolver.base import Resolver


class RegistryResolver(Resolver):
    def can_resolve(self, ref: str) -> bool:
        # simple heuristic for now
        return "/" in ref and ":" in ref

    def resolve(self, ref: str) -> str:
        raise NotImplementedError("Registry not implemented yet")
