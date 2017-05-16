from contract_parser.nodes.Node import Node
from typing import Iterable, Tuple

from contract_parser.tokens.Token import Token


class Tree:
    def __init__(self, roots: Iterable[Node] = None):
        self.roots = [] if roots is None else list(roots)

    def __str__(self) -> str:
        result = []
        for root in self.roots:
            result.extend(root.str(0))
        return "\n".join(result)

    def flatten(self) -> Iterable[Tuple[Token, str]]:
        result = []
        for root in self.roots:
            result.extend(root.flatten())
        return result
