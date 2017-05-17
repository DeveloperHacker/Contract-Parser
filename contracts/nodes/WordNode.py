from typing import Iterable

from contracts.nodes.Node import Node
from contracts.parser.Instruction import Instruction
from contracts.tokens import tokens


class WordNode(Node):
    def __init__(self, instance: str):
        super().__init__(tokens.WORD)
        self.instance = instance

    def str(self, depth: int) -> Iterable[str]:
        return [" " * depth + self.token.name + " ~ " + self.instance]

