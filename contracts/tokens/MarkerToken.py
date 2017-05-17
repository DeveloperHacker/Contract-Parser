from contracts.tokens.Token import Token


class MarkerToken(Token):
    instances = {}

    def __init__(self, name: str):
        super().__init__(name)
        MarkerToken.instances[name] = self

    @staticmethod
    def is_marker(string: str) -> bool:
        return string in MarkerToken.instances
