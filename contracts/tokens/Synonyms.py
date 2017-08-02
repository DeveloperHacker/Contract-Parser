from typing import Dict, List

from contracts.tokens import Labels
from contracts.tokens.SynonymToken import SynonymToken
from contracts.tokens.Token import Token

instances: Dict[str, Token] = {}
names: List[str] = []

SHORT_WEAK = SynonymToken("`", Labels.WEAK)
