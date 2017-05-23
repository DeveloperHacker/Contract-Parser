from contracts.tokens.Token import Token


class Instruction:
    _max_id = 0

    def __init__(self, token: Token, word: str = None):
        self.token = token
        self.word = word
        Instruction._max_id += 1
        self.id = Instruction._max_id

    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, Instruction):
            return self.id == other.id
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __str__(self) -> str:
        if self.word is None:
            return self.token.name
        else:
            return "{} ~ {}".format(self.token.name, self.word)
