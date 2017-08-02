from typing import Dict, List

from contracts.tokens.MarkerToken import MarkerToken
from contracts.tokens.StringToken import StringToken
from contracts.tokens.Token import Token

instances: Dict[str, Dict[int, Token]] = {}
names: List[str] = []

RESULT = MarkerToken("result")
ZERO = MarkerToken("0")
NULL = MarkerToken("null")
TRUE = MarkerToken("true")
FALSE = MarkerToken("false")
THIS = MarkerToken("this")
PRE_THIS = MarkerToken("pre_this")
POST_THIS = MarkerToken("post_this")

PARAM = MarkerToken("param")
PARAM_0 = MarkerToken("param[0]")
PARAM_1 = MarkerToken("param[1]")
PARAM_2 = MarkerToken("param[2]")
PARAM_3 = MarkerToken("param[3]")
PARAM_4 = MarkerToken("param[4]")

STRING = StringToken("string")
