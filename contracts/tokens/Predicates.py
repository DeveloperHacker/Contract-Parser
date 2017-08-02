from typing import Dict, List

from contracts.tokens.PredicateToken import PredicateToken

instances: Dict[str, PredicateToken] = {}
names: List[str] = []

LOWER = PredicateToken("lower", 2)
GREATER = PredicateToken("greater", 2)
LOWER_OR_EQUAL = PredicateToken("leq", 2)
GREATER_OR_EQUAL = PredicateToken("geq", 2)
EQUAL = PredicateToken("equal", 2)
NOT_EQUAL = PredicateToken("not_equal", 2)
FOLLOW = PredicateToken("follow", 2)
MAYBE = PredicateToken("maybe", 2)
GET = PredicateToken("get", 2)
IS = PredicateToken("is", 2)
IS_NOT = PredicateToken("is_not", 2)
