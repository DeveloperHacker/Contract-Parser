import re
from typing import Dict, List, Union

from contracts.tokens import Synonyms
from contracts.tokens.MarkerToken import MarkerToken
from contracts.tokens.StringToken import StringToken


def _expand(string: str) -> (str, int):
    matched = re.match(r"([\w\_]+)\[(.+)\]", string)
    return matched.groups() if matched else (string, -1)


def value_of(string: str) -> Union[MarkerToken, None]:
    if string in Synonyms.instances:
        instance = Synonyms.instances[string]
        if isinstance(instance, MarkerToken):
            return instance
    if string in instances:
        return instances[string][-1]
    family_name, index = _expand(string)
    if family_name not in instances:
        return None
    if index not in instances[family_name]: index = -1
    return instances[family_name][index]


instances: Dict[str, Dict[int, MarkerToken]] = {}
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
