from typing import Iterable

from contracts.nodes.Ast import Ast


class Forest:
    def __init__(self, trees: Iterable[Ast] = None):
        self.trees = [] if trees is None else list(trees)

    def __str__(self) -> str:
        result = []
        for tree in self.trees:
            result.append(str(tree))
        return "\n".join(result)
