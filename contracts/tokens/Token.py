from abc import ABCMeta


class Token(metaclass=ABCMeta):
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, Token):
            return self.name == other.name
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
