import re

from typing import Dict

from contracts.tokens.LabelToken import LabelToken
from contracts.tokens.MarkerToken import MarkerToken
from contracts.tokens.PredicateToken import PredicateToken
from contracts.tokens.Token import Token

_instances: Dict[str, Dict[int, 'Token']] = {}


def instances():
    for family_name, family in _instances.items():
        for index, token in family.items():
            yield token.name


def register(*tokens):
    for token in tokens:
        family_name, index = expand(token.name)
        if family_name not in _instances:
            _instances[family_name] = {}
        _instances[family_name][index] = token


def expand(string: str) -> (str, int):
    matched = re.match(r"(@[\w\_]+)\[(.+)\]", string)
    return matched.groups() if matched else (string, -1)


def is_token(string: str) -> bool:
    family_name, index = expand(string)
    return family_name in _instances


def value_of(string: str) -> 'Token':
    family_name, index = expand(string)
    if family_name not in _instances: raise ValueError
    if index not in _instances[family_name]: index = -1
    return _instances[family_name][index]


# -------------------- Functions -------------------- #
LOWER = PredicateToken("lower", 2)
GREATER = PredicateToken("greater", 2)
EQUAL = PredicateToken("equal", 2)
NOT_EQUAL = PredicateToken("not_equal", 2)
FOLLOW = PredicateToken("follow", 2)
MAYBE = PredicateToken("maybe", 2)
register(LOWER, GREATER, EQUAL, NOT_EQUAL, FOLLOW, MAYBE)

# -------------------- Variables -------------------- #
RESULT = MarkerToken("@result")
PARAM = MarkerToken("@param")
PARAM_0 = MarkerToken("@param[0]")
PARAM_1 = MarkerToken("@param[1]")
PARAM_2 = MarkerToken("@param[2]")
PARAM_3 = MarkerToken("@param[3]")
PARAM_4 = MarkerToken("@param[4]")
STRING = MarkerToken("@string")
WORD = MarkerToken("@word")
ZERO = MarkerToken("@zero")
NULL = MarkerToken("@null")
TRUE = MarkerToken("@true")
FALSE = MarkerToken("@false")
END = MarkerToken("@end")
register(RESULT, PARAM, PARAM_0, PARAM_1, PARAM_2, PARAM_3, PARAM_4, ZERO, WORD, STRING, NULL, TRUE, FALSE, END)

# -------------------- Labels -------------------- #
STRONG = LabelToken("strong")
WEAK = LabelToken("weak")
register(STRONG, WEAK)

# -------------------- Brackets -------------------- #
LB = "("
RB = ")"
