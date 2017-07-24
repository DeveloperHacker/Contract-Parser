import re
from typing import Dict, Union

from contracts.tokens.LabelToken import LabelToken
from contracts.tokens.MarkerToken import MarkerToken
from contracts.tokens.OperatorToken import OperatorToken
from contracts.tokens.PredicateToken import PredicateToken
from contracts.tokens.StringToken import StringToken
from contracts.tokens.SynonymToken import SynonymToken
from contracts.tokens.Token import Token

_markers: Dict[str, Dict[int, Token]] = {}
_predicates: Dict[str, PredicateToken] = {}
_operators: Dict[str, OperatorToken] = {}
_labels: Dict[str, LabelToken] = {}
_synonyms: Dict[str, Token] = {}


def predicates():
    for name, _ in _predicates.items():
        yield name


def markers():
    for family_name, family in _markers.items():
        for index, token in family.items():
            yield token.name


def operators():
    for name, _ in _operators.items():
        yield name


def labels():
    for name, _ in _labels.items():
        yield name


def synonyms():
    for name, _ in _synonyms.items():
        yield name


def register(token: Token):
    if isinstance(token, SynonymToken):
        _synonyms[token.name] = token.meaning
    elif isinstance(token, OperatorToken):
        _operators[token.name] = token
    elif isinstance(token, LabelToken):
        _labels[token.name] = token
    elif isinstance(token, PredicateToken):
        _predicates[token.name] = token
    elif isinstance(token, MarkerToken):
        family_name, index = expand(token.name)
        if family_name not in _markers:
            _markers[family_name] = {}
        _markers[family_name][index] = token
    else:
        raise ValueError


def expand(string: str) -> (str, int):
    matched = re.match(r"([\w\_]+)\[(.+)\]", string)
    return matched.groups() if matched else (string, -1)


def value_of(string: str) -> Union[Token, None]:
    if string in _operators:
        return _operators[string]
    elif string in _synonyms:
        return _synonyms[string]
    elif string in _labels:
        return _labels[string]
    elif string in _predicates:
        return _predicates[string]
    elif string in _markers:
        return _markers[string][-1]
    else:
        family_name, index = expand(string)
        if family_name not in _markers:
            return None
        if index not in _markers[family_name]: index = -1
        return _markers[family_name][index]


# -------------------- Functions -------------------- #
LOWER = PredicateToken("lower", 2)
GREATER = PredicateToken("greater", 2)
LOWER_OR_EQUAL = PredicateToken("leq", 2)
GREATER_OR_EQUAL = PredicateToken("geq", 2)
EQUAL = PredicateToken("equal", 2)
NOT_EQUAL = PredicateToken("not_equal", 2)
FOLLOW = PredicateToken("follow", 2)
MAYBE = PredicateToken("maybe", 2)
GET = PredicateToken("get", 2)
register(LOWER)
register(GREATER)
register(LOWER_OR_EQUAL)
register(GREATER_OR_EQUAL)
register(EQUAL)
register(NOT_EQUAL)
register(FOLLOW)
register(MAYBE)
register(GET)

# -------------------- Operators -------------------- #
EQUAL_OP = OperatorToken("==", EQUAL)
NOT_EQUAL_OP = OperatorToken("!=", NOT_EQUAL)
MAYBE_OP = OperatorToken("?=", MAYBE)
LOWER_OP = OperatorToken("<", LOWER)
GREATER_OP = OperatorToken(">", GREATER)
LOWER_OR_EQUAL_OP = OperatorToken("<=", LOWER_OR_EQUAL)
GREATER_OR_EQUAL_OP = OperatorToken(">=", GREATER_OR_EQUAL)
FOLLOW_OP = OperatorToken("=>", FOLLOW)
GET_OP = OperatorToken(".", GET)
register(LOWER_OP)
register(GREATER_OP)
register(LOWER_OR_EQUAL_OP)
register(GREATER_OR_EQUAL_OP)
register(EQUAL_OP)
register(NOT_EQUAL_OP)
register(FOLLOW_OP)
register(MAYBE_OP)
register(GET_OP)

# -------------------- Markers -------------------- #
RESULT = MarkerToken("result")
ZERO = MarkerToken("0")
NULL = MarkerToken("null")
TRUE = MarkerToken("true")
FALSE = MarkerToken("false")
THIS = MarkerToken("this")
PRE_THIS = MarkerToken("pre_this")
POST_THIS = MarkerToken("post_this")
register(RESULT)
register(ZERO)
register(NULL)
register(TRUE)
register(FALSE)
register(THIS)
register(PRE_THIS)
register(POST_THIS)

PARAM = MarkerToken("param")
PARAM_0 = MarkerToken("param[0]")
PARAM_1 = MarkerToken("param[1]")
PARAM_2 = MarkerToken("param[2]")
PARAM_3 = MarkerToken("param[3]")
PARAM_4 = MarkerToken("param[4]")
register(PARAM)
register(PARAM_0)
register(PARAM_1)
register(PARAM_2)
register(PARAM_3)
register(PARAM_4)

# -------------------- String -------------------- #
STRING = StringToken("string")
register(STRING)

# -------------------- Labels -------------------- #
STRONG = LabelToken("strong")
WEAK = LabelToken("weak")
register(STRONG)
register(WEAK)

# -------------------- Synonyms -------------------- #
SHORT_WEAK = SynonymToken("`", WEAK)
register(SHORT_WEAK)

# -------------------- Brackets -------------------- #
LB = "("
RB = ")"
