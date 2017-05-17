from typing import Iterable, List

from contracts.tokens.Token import Token


class Node:
    def __init__(self, token: Token = None, children: Iterable['Node'] = None):
        self.token = token
        self.children: List[Node] = [] if children is None else list(children)

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def str(self, depth: int) -> List[str]:
        result: List[str] = [" " * depth + self.token.name]
        if not self.is_leaf():
            for child in self.children:
                result.extend(child.str(depth + 1))
        return result
