from contracts.nodes.Ast import Ast
from contracts.nodes.Node import Node
from contracts.nodes.StringNode import StringNode
from contracts.visitors.AstVisitor import AstVisitor


class AstDecompiler(AstVisitor):
    def __init__(self):
        super().__init__()
        self._tokens = None
        self._stack = None
        self._result = None
        self._token_name = None

    def result(self) -> str:
        if self._tokens is None:
            raise ValueError()
        return self._result

    def visit(self, ast: Ast):
        self._tokens = []
        self._stack = []

    def visit_end(self, ast: Ast):
        self._result = "{} {}".format(ast.label.name, self._tokens[0])

    def visit_node(self, node: Node):
        self._stack.append((self._token_name, self._tokens))
        self._tokens = []
        self._token_name = node.token.name

    def visit_string(self, node: StringNode):
        self._token_name = "\"{}\"".format(" ".join(node.words))

    def visit_node_end(self, node: Node):
        string = self._token_name
        if len(self._tokens) > 0:
            string += "(" + ", ".join(self._tokens) + ")"
        self._token_name, self._tokens = self._stack.pop()
        self._tokens.append(string)
