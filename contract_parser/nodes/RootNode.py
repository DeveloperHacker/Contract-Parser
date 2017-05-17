from typing import Iterable, List

from contract_parser.Instruction import Instruction
from contract_parser.nodes.Node import Node
from contract_parser.tokens.Token import Token


class RootNode(Node):
    def __init__(self, token: Token = None, child: Node = None):
        super().__init__(token, [child] if child else None)

    def flatten(self) -> Iterable[Instruction]:
        result: List[Instruction] = [Instruction(self.token)]
        for child in self.children:
            result.extend(child.flatten())
        return result
