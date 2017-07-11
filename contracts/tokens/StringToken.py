from contracts.tokens.MarkerToken import MarkerToken


class StringToken(MarkerToken):
    def __init__(self, name: str):
        super().__init__(name)
