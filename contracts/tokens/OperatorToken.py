from typing import Union, Iterable

from contracts.tokens.PredicateToken import PredicateToken
from contracts.tokens.Token import Token


class OperatorToken(Token):
    def __init__(self, name: str, predicate: Union[PredicateToken, Iterable[PredicateToken]]):
        super().__init__(name)
        self.predicate = predicate
        self.predicate = list(self.predicate) if isinstance(self.predicate, Iterable) else [self.predicate]
