from typing import Iterable

from parser.Token import Token


class Node:
    def __init__(self, token: Token, children: Iterable['Node']):
        self.token = token
        self.children = tuple(children)

    def is_leaf(self) -> bool:
        return len(self.children) == 0
