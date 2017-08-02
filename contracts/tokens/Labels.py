from typing import Dict, List

from contracts.tokens.LabelToken import LabelToken

instances: Dict[str, LabelToken] = {}
names: List[str] = []

STRONG = LabelToken("strong")
WEAK = LabelToken("weak")
