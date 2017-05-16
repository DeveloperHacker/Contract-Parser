from typing import Iterable, Tuple

from src.parser.nodes.Node import Node
from src.parser.tokens import tokens
from src.parser.tokens.Token import Token


class StringNode(Node):
    def __init__(self, token: Token = None, children: Iterable[Node] = None):
        super().__init__(token, children)

    def flatten(self) -> Iterable[Tuple[Token, str]]:
        result = []
        for child in self.children:
            result.extend(child.flatten())
        result.append((tokens.END_STRING, None))
        return result
