import enum
from enum import Enum

from typing import Iterable

from contract_parser.tokens.Token import Token


class Type(Enum):
    ARGUMENT = enum.auto()
    VARARG = enum.auto()


class FunctionToken(Token):
    instances = {}

    def __init__(self, name: str, arguments: Iterable[Type]):
        super().__init__(name)
        self.arguments = tuple(arguments)
        self.min_num_arguments = len(self.arguments)
        self.max_num_arguments = sum(float("inf") if arg is Type.VARARG else 1 for arg in self.arguments)
        FunctionToken.instances[name] = self

    @staticmethod
    def is_function(string: str) -> bool:
        return string in FunctionToken.instances
