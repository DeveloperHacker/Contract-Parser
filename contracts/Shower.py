from typing import List

from contracts.DfsGuide import DfsGuide
from contracts.Node import Node
from contracts.Token import Token
from contracts.Tokens import *
from contracts.TreeVisitor import TreeVisitor


def priority(token: Token) -> int:
    if token.name in (EQUAL, NOT_EQUAL, MAY, IS, IS_NOT, GREATER_OR_EQUAL, GREATER, LOWER_OR_EQUAL, LOWER):
        return 1
    if token.name == AND:
        return 2
    if token.name == OR:
        return 3
    if token.name == FOLLOW:
        return 4
    return 10


class Shower(TreeVisitor):
    def __init__(self):
        super().__init__(DfsGuide())
        self._result = []

    def result(self) -> List[str]:
        return self._result

    def visit_operator_end(self, depth: int, node: Node, parent: Node):
        cond = node.children[1].token.type == Types.MARKER
        cond &= node.children[1].token.name[1:-1].isalpha()
        cond |= node.children[0].token.type == Types.MARKER
        right = self._result.pop()
        left = self._result.pop()
        if node.token.name == GETATTR and not cond:
            string = "get(" + left + ", " + right + ")"
        else:
            cond1 = priority(node.token) < priority(parent.token)
            cond2 = node.token.name == GETATTR
            string1 = "%s" if cond1 else "(%s)"
            string2 = "%s" if cond2 else " %s "
            string = string1 % (left + string2 + right) % node.token.name
        self._result.append(string)

    def visit_marker(self, depth: int, node: Node, parent: Node):
        self._result.append(node.token.name)

    def visit_string(self, depth: int, node: Node, parent: Node):
        self._result.append(node.token.name)

    def visit_label_end(self, depth: int, node: Node, parent: Node):
        string = self._result.pop()
        self._result.append(node.token.name + " " + string)
