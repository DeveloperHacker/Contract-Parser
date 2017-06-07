from contracts.tokens.Token import Token


class PredicateToken(Token):
    def __init__(self, name: str, num_arguments: int):
        super().__init__(name)
        self.num_arguments = num_arguments
