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
        family_name, index = Markers._expand(token.name)
        if family_name not in Markers.instances:
            Markers.instances[family_name] = {}
        Markers.instances[family_name][index] = token
        Markers.names.append(token.name)
    else:
        raise ValueError


def __lazy_function(func):
    _object = {}

    def _function(*args, **kwargs):
        if "instance" not in _object:
            _object["instance"] = func(*args, **kwargs)
        return _object["instance"]

    return _function


@__lazy_function
def register_all_tokens():
    register(Predicates.GET)
    register(Predicates.EQUAL)
    register(Predicates.NOT_EQUAL)
    register(Predicates.MAY)
    register(Predicates.LOWER_OR_EQUAL)
    register(Predicates.LOWER)
    register(Predicates.FOLLOW)
    register(Predicates.IS)
    register(Predicates.IS_NOT)

    register(Operators.GET)
    register(Operators.EQUAL)
    register(Operators.NOT_EQUAL)
    register(Operators.MAY)
    register(Operators.LOWER_OR_EQUAL)
    register(Operators.LOWER)
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
    register(Labels.SHORT_WEAK)


register_all_tokens()
