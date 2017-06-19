from typing import Iterable, List

from contracts.tokens.Token import Token


class Node:
    def __init__(self, token: Token, children: Iterable['Node'] = None):
        self.token = token
        self.children = [] if children is None else list(children)

    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, Node):
            if len(self.children) != len(other.children):
                return False
            for child, other_child in zip(self.children, other.children):
                if child != other_child:
                    return False
            return self.token == other.token
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def str(self, depth: int) -> List[str]:
        result: List[str] = [" " * depth + self.token.name]
        if not self.is_leaf():
            for child in self.children:
                result.extend(child.str(depth + 1))
        return result
