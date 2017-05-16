from abc import ABCMeta


class Token(metaclass=ABCMeta):
    instances = {}

    def __init__(self, name: str):
        self.name = name
        Token.instances[name] = self

    @staticmethod
    def is_token(string: str) -> bool:
        return string in Token.instances

    @staticmethod
    def value_of(string: str) -> 'Token':
        return Token.instances[string]
