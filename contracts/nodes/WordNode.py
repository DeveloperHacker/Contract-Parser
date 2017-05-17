from typing import List

from contracts.nodes.Node import Node
from contracts.tokens import tokens


class WordNode(Node):
    def __init__(self, instance: str):
        super().__init__(tokens.WORD)
        self.instance = instance

    def str(self, depth: int) -> List[str]:
        return [" " * depth + self.token.name + " ~ " + self.instance]
