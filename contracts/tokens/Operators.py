from typing import Dict, List, Union

from contracts.tokens import Predicates, Synonyms
from contracts.tokens.OperatorToken import OperatorToken


def value_of(string: str) -> Union[OperatorToken, None]:
    if string in Synonyms.instances:
        instance = Synonyms.instances[string]
        if isinstance(instance, OperatorToken):
            return instance
    if string in instances:
        return instances[string]


instances: Dict[str, OperatorToken] = {}
names: List[str] = []

EQUAL = OperatorToken("==", Predicates.EQUAL)
NOT_EQUAL = OperatorToken("!=", Predicates.NOT_EQUAL)
MAY = OperatorToken("?=", Predicates.MAY)
LOWER = OperatorToken("<", Predicates.LOWER)
LOWER_OR_EQUAL = OperatorToken("<=", Predicates.LOWER_OR_EQUAL)
FOLLOW = OperatorToken("=>", Predicates.FOLLOW)
GET = OperatorToken(".", Predicates.GET)
IS = OperatorToken("is", Predicates.IS)
IS_NOT = OperatorToken("is not", Predicates.IS_NOT)
