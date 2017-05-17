from typing import Iterable

from contract_parser.Instruction import Instruction
from contract_parser.nodes.Node import Node
from contract_parser.tokens import tokens


class WordNode(Node):
    def __init__(self, instance: str):
        super().__init__(tokens.WORD)
        self.instance = instance

    def str(self, depth: int) -> Iterable[str]:
        return [" " * depth + self.token.name + " ~ " + self.instance]

    def flatten(self) -> Iterable[Instruction]:
        return [Instruction(self.token, self.instance)]
