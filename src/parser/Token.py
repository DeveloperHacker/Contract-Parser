import enum
from abc import ABCMeta
from enum import Enum

from typing import Iterable


class Type(Enum):
    ARGUMENT = enum.auto()
    VARARG = enum.auto()


class Token(metaclass=ABCMeta):
    def __init__(self, name: str):
        self.name = name


class Variable(Token):
    def __init__(self, name: str):
        super().__init__(name)


class Function(Token):
    def __init__(self, name: str, arguments: Iterable[Type]):
        super().__init__(name)
        self.arguments = tuple(arguments)


class Label(Token):
    def __init__(self, name: str):
        super().__init__(name)


EQUAL = Function("equal", Type.ARGUMENT, Type.ARGUMENT)
NOT_EQUAL = Function("not_equal", Type.ARGUMENT, Type.ARGUMENT)
IS = Function("is", Type.ARGUMENT, Type.ARGUMENT)
FOLLOW = Function("follow", Type.ARGUMENT, Type.ARGUMENT)
MAYBE = Function("maybe", Type.ARGUMENT, Type.ARGUMENT)
AND = Function("and", Type.ARGUMENT, Type.VARARG)
OR = Function("or", Type.ARGUMENT, Type.VARARG)
INSIDE = Function("inside", Type.ARGUMENT, Type.VARARG)
LOWER = Function("lower", Type.ARGUMENT, Type.ARGUMENT)
GREATER = Function("greater", Type.ARGUMENT, Type.ARGUMENT)
SATISFY = Function("satisfy", Type.ARGUMENT, Type.ARGUMENT)

PARAM_1 = Variable("@param[1]")
PARAM_2 = Variable("@param[3]")
PARAM_3 = Variable("@param[4]")
PARAM_4 = Variable("@param[5]")
PARAM_5 = Variable("@param[6]")
PARAM = Variable("@param")
NUMBER_0 = Variable("@number[0]")
NUMBER_1 = Variable("@number[1]")
NUMBER_2 = Variable("@number[2]")
NUMBER_3 = Variable("@number[3]")
NUMBER_4 = Variable("@number[4]")
NUMBER_5 = Variable("@number[5]")
NUMBER_6 = Variable("@number[6]")
NUMBER_7 = Variable("@number[7]")
NUMBER_8 = Variable("@number[8]")
NUMBER_9 = Variable("@number[9]")
NUMBER = Variable("@number")
RESULT = Variable("@result")
NULL = Variable("@null")
TRUE = Variable("@true")
FALSE = Variable("@false")

STRONG = Label("strong")
WEAK = Label("weak")
