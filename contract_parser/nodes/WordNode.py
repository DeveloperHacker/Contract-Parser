from contract_parser.nodes.Node import Node
from contract_parser.tokens import tokens
from typing import Iterable, Tuple

from contract_parser.tokens.Token import Token


class WordNode(Node):
    def __init__(self, instance: str):
        super().__init__(tokens.WORD)
        self.instance = instance

    def str(self, depth: int) -> Iterable[str]:
        return [" " * depth + self.token.name + " " + self.instance]

    def flatten(self) -> Iterable[Tuple[Token, str]]:
        return [(self.token, self.instance)]
