from typing import Iterable, List

from contracts.nodes.Node import Node
from contracts.nodes.WordNode import WordNode
from contracts.tokens import tokens


class StringNode(Node):
    def __init__(self, children: Iterable[WordNode] = None):
        super().__init__(tokens.STRING, children)

    def str(self, depth: int):
        result: List[str] = [" " * depth + self.token.name + " {"]
        for child in self.children:
            result.extend(child.str(depth + 1))
        result.append(" " * depth + "}")
        return result
