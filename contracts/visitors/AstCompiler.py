from typing import List

from contracts.nodes.Ast import Ast
from contracts.nodes.Node import Node
from contracts.nodes.StringNode import StringNode
from contracts.tokens.LabelToken import LabelToken
from contracts.tokens.Token import Token
from contracts.visitors.AstVisitor import AstVisitor


class AstCompiler(AstVisitor):
    def __init__(self):
        super().__init__()
        self._label = None
        self._tokens = None
        self._strings = None

    def result(self) -> (LabelToken, List[Token]):
        return self._label, self._tokens, self._strings

    def visit(self, ast: Ast):
        self._label = ast.label
        self._tokens = []
        self._strings = {}

    def visit_node(self, node: Node):
        self._tokens.append(node.token)

    def visit_string(self, node: StringNode):
        idx = len(self._tokens) - 1
        self._strings[idx] = node.words
