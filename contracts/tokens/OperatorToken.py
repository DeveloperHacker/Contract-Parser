from contracts.tokens.PredicateToken import PredicateToken
from contracts.tokens.Token import Token


class OperatorToken(Token):
    def __init__(self, name: str, predicate: PredicateToken):
        super().__init__(name)
        self.predicate = predicate
