from typing import Iterable, Tuple

from src.parser.nodes.Node import Node
from src.parser.tokens import tokens
from src.parser.tokens.Token import Token


class WordNode(Node):
    def __init__(self, instance: str):
        super().__init__(tokens.WORD)
        self.instance = instance

    def str(self, depth: int) -> Iterable[str]:
        return [" " * depth + self.token.name + " " + self.instance]

    def flatten(self) -> Iterable[Tuple[Token, str]]:
        return [(self.token, self.instance)]
