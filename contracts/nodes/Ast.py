from typing import Iterable

from contracts.nodes.Node import Node


class Ast:
    def __init__(self, roots: Iterable[Node] = None):
        self.roots = [] if roots is None else list(roots)

    def __str__(self) -> str:
        result = []
        for root in self.roots:
            result.extend(root.str(0))
        return "\n".join(result)
