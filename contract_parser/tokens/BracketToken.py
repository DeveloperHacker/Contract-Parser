from contract_parser.tokens.Token import Token


class BracketToken(Token):
    instances = {}

    def __init__(self, name: str):
        super().__init__(name)
        BracketToken.instances[name] = self
