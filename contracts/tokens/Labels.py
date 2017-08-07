from typing import Dict, List, Union

from contracts.tokens import Synonyms
from contracts.tokens.LabelToken import LabelToken
from contracts.tokens.SynonymToken import SynonymToken


def value_of(string: str) -> Union[LabelToken, None]:
    if string in Synonyms.instances:
        instance = Synonyms.instances[string]
        if isinstance(instance, LabelToken):
            return instance
    if string in instances:
        return instances[string]


instances: Dict[str, LabelToken] = {}
names: List[str] = []

STRONG = LabelToken("strong")
WEAK = LabelToken("weak")

SHORT_WEAK = SynonymToken("`", WEAK)
