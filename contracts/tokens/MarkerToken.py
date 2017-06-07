from contracts.tokens.Token import Token


class MarkerToken(Token):
    def __init__(self, name: str):
        super().__init__(name)
