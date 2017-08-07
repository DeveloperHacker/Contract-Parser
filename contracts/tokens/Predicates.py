from typing import Dict, List, Union

from contracts.tokens import Synonyms
from contracts.tokens.PredicateToken import PredicateToken


def value_of(string: str) -> Union[PredicateToken, None]:
    if string in Synonyms.instances:
        instance = Synonyms.instances[string]
        if isinstance(instance, PredicateToken):
            return instance
    if string in instances:
        return instances[string]


instances: Dict[str, PredicateToken] = {}
names: List[str] = []

LOWER = PredicateToken("lower", 2)
LOWER_OR_EQUAL = PredicateToken("leq", 2)
EQUAL = PredicateToken("equal", 2)
NOT_EQUAL = PredicateToken("not_equal", 2)
FOLLOW = PredicateToken("follow", 2)
MAY = PredicateToken("may", 2)
GET = PredicateToken("get", 2)
IS = PredicateToken("is", 2)
IS_NOT = PredicateToken("is_not", 2)
