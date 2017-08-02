import re
from typing import Union

from contracts.tokens import Labels
from contracts.tokens import Markers
from contracts.tokens import Operators
from contracts.tokens import Predicates
from contracts.tokens import Synonyms
from contracts.tokens.LabelToken import LabelToken
from contracts.tokens.MarkerToken import MarkerToken
from contracts.tokens.OperatorToken import OperatorToken
from contracts.tokens.PredicateToken import PredicateToken
from contracts.tokens.SynonymToken import SynonymToken
from contracts.tokens.Token import Token


def _expand(string: str) -> (str, int):
    matched = re.match(r"([\w\_]+)\[(.+)\]", string)
    return matched.groups() if matched else (string, -1)


def register(token: Token):
    if isinstance(token, SynonymToken):
        Synonyms.instances[token.name] = token.meaning
        Synonyms.names.append(token.name)
    elif isinstance(token, OperatorToken):
        Operators.instances[token.name] = token
        Operators.names.append(token.name)
    elif isinstance(token, LabelToken):
        Labels.instances[token.name] = token
        Labels.names.append(token.name)
    elif isinstance(token, PredicateToken):
        Predicates.instances[token.name] = token
        Predicates.names.append(token.name)
    elif isinstance(token, MarkerToken):
        family_name, index = _expand(token.name)
        if family_name not in Markers.instances:
            Markers.instances[family_name] = {}
        Markers.instances[family_name][index] = token
        Markers.names.append(token.name)
    else:
        raise ValueError


def value_of(string: str) -> Union[Token, None]:
    if string in Operators.instances:
        return Operators.instances[string]
    elif string in Synonyms.instances:
        return Synonyms.instances[string]
    elif string in Labels.instances:
        return Labels.instances[string]
    elif string in Predicates.instances:
        return Predicates.instances[string]
    elif string in Markers.instances:
        return Markers.instances[string][-1]
    else:
        family_name, index = _expand(string)
        if family_name not in Markers.instances:
            return None
        if index not in Markers.instances[family_name]: index = -1
        return Markers.instances[family_name][index]


register(Predicates.GET)
register(Predicates.EQUAL)
register(Predicates.NOT_EQUAL)
register(Predicates.MAYBE)
register(Predicates.LOWER_OR_EQUAL)
register(Predicates.GREATER_OR_EQUAL)
register(Predicates.LOWER)
register(Predicates.GREATER)
register(Predicates.FOLLOW)
register(Predicates.IS)
register(Predicates.IS_NOT)

register(Operators.GET)
register(Operators.EQUAL)
register(Operators.NOT_EQUAL)
register(Operators.MAYBE)
register(Operators.LOWER_OR_EQUAL)
register(Operators.GREATER_OR_EQUAL)
register(Operators.LOWER)
register(Operators.GREATER)
register(Operators.FOLLOW)
register(Operators.IS)
register(Operators.IS_NOT)

register(Markers.RESULT)
register(Markers.ZERO)
register(Markers.NULL)
register(Markers.TRUE)
register(Markers.FALSE)
register(Markers.THIS)
register(Markers.PRE_THIS)
register(Markers.POST_THIS)

register(Markers.PARAM_4)
register(Markers.PARAM_3)
register(Markers.PARAM_2)
register(Markers.PARAM_1)
register(Markers.PARAM_0)
register(Markers.PARAM)

register(Markers.STRING)

register(Labels.STRONG)
register(Labels.WEAK)

register(Synonyms.SHORT_WEAK)
