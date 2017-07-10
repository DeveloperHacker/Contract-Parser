from contracts.tokens.Token import Token


class SynonymToken(Token):
    def __init__(self, name: str, synonym: Token):
        super().__init__(name)
        self._synonym = synonym

    @property
    def meaning(self) -> Token:
        synonym = self._synonym
        while isinstance(synonym, SynonymToken):
            synonym = self._synonym
        return synonym
