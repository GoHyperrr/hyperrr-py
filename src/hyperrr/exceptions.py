class HyperrrError(Exception):
    pass


class PromptParseError(HyperrrError):
    pass


class PromptRenderError(HyperrrError):
    pass


class PromptResolutionError(HyperrrError):
    pass
