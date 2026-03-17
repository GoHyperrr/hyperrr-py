class Resolver:
    def can_resolve(self, ref: str) -> bool:
        raise NotImplementedError

    def resolve(self, ref: str) -> str:
        raise NotImplementedError
