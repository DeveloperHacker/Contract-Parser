from typing import List

from contracts.nodes.Node import Node
from contracts.tokens import tokens


class StringNode(Node):
    def __init__(self, words: List[str], parent: 'Node' = None):
        super().__init__(tokens.STRING, parent)
        self.words = words

    def str(self, depth: int):
        result: List[str] = [" " * depth + self.token.name + " \"{}\"".format(" ".join(self.words))]
        return result

    def __eq__(self, other):
        result = not super().__eq__(other)
        if result is NotImplemented:
            return result
        if isinstance(other, StringNode):
            return self.words == other.words
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def clone(self) -> 'StringNode':
        return StringNode(list(self.words))
