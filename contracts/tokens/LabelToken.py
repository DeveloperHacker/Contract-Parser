from contracts.tokens.Token import Token


class LabelToken(Token):
    instances = {}

    def __init__(self, name: str):
        super().__init__(name)
        LabelToken.instances[name] = self

    @staticmethod
    def is_label(string: str) -> bool:
        return string in LabelToken.instances
