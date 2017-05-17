from typing import Iterable, List

from contract_parser.Instruction import Instruction
from contract_parser.nodes.Node import Node
from contract_parser.nodes.WordNode import WordNode
from contract_parser.tokens import tokens
from contract_parser.tokens.MarkerToken import MarkerToken


class StringNode(Node):
    def __init__(self, token: MarkerToken = None, children: Iterable[WordNode] = None):
        super().__init__(token, children)

    def str(self, depth: int):
        result: List[str] = [" " * depth + self.token.name + " {"]
        for child in self.children:
            result.extend(child.str(depth + 1))
        result.append(" " * depth + "}")
        return result

    def flatten(self) -> Iterable[Instruction]:
        result: List[Instruction] = []
        for child in self.children:
            result.extend(child.flatten())
        result.append(Instruction(tokens.END_STRING))
        return result
