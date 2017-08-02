from typing import Dict, List

from contracts.tokens import Predicates
from contracts.tokens.OperatorToken import OperatorToken

instances: Dict[str, OperatorToken] = {}
names: List[str] = []

EQUAL = OperatorToken("==", Predicates.EQUAL)
NOT_EQUAL = OperatorToken("!=", Predicates.NOT_EQUAL)
MAYBE = OperatorToken("?=", Predicates.MAYBE)
LOWER = OperatorToken("<", Predicates.LOWER)
GREATER = OperatorToken(">", Predicates.GREATER)
LOWER_OR_EQUAL = OperatorToken("<=", Predicates.LOWER_OR_EQUAL)
GREATER_OR_EQUAL = OperatorToken(">=", Predicates.GREATER_OR_EQUAL)
FOLLOW = OperatorToken("=>", Predicates.FOLLOW)
GET = OperatorToken(".", Predicates.GET)
IS = OperatorToken("is", Predicates.IS)
IS_NOT = OperatorToken("is not", Predicates.IS_NOT)
