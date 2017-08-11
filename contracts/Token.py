class Token:
    def __init__(self, name: str, token_type: str):
        self.name = name
        self.type = token_type

    def __str__(self):
        return self.type + "(%s)" % self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, Token):
            return self.name == other.name and self.type == other.type
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
