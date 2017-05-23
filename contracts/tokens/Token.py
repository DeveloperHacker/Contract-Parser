import re
from abc import ABCMeta

from typing import Dict


class Token(metaclass=ABCMeta):
    instances: Dict[str, Dict[int, 'Token']] = {}

    def __init__(self, name: str):
        family_name, index = Token.expand(name)
        self.name = name
        self.family_name = family_name
        self.index = index
        if family_name not in Token.instances:
            Token.instances[family_name] = {}
        Token.instances[family_name][index] = self

    @staticmethod
    def expand(string: str) -> (str, int):
        matched = re.match(r"(@[a-zA-Z]+)\[(.+)\]", string)
        return matched.groups() if matched else (string, -1)

    @staticmethod
    def is_token(string: str) -> bool:
        family_name, index = Token.expand(string)
        return family_name in Token.instances

    @staticmethod
    def value_of(string: str) -> 'Token':
        family_name, index = Token.expand(string)
        if family_name not in Token.instances: raise ValueError
        if index not in Token.instances[family_name]: index = -1
        return Token.instances[family_name][index]

    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, Token):
            return self.family_name == other.family_name and self.index == other.index
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
