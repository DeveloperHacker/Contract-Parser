from contract_parser.nodes.Node import Node
from typing import Iterable, Tuple, List

from contract_parser.tokens.Token import Token


class RootNode(Node):
    def __init__(self, token: Token = None, child: Node = None):
        super().__init__(token, [child] if child else None)

    def flatten(self) -> Iterable[Tuple[Token, str]]:
        result: List[Tuple[Token, str]] = [(self.token, None)]
        for child in self.children:
            result.extend(child.flatten())
        return result
