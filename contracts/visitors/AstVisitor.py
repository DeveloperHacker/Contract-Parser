from abc import ABCMeta

from contracts.nodes.Ast import Ast
from contracts.nodes.Node import Node
from contracts.nodes.StringNode import StringNode


class AstVisitor(metaclass=ABCMeta):
    def result(self):
        return None

    def visit(self, ast: Ast):
        pass

    def visit_end(self, ast: Ast):
        pass

    def visit_node(self, node: Node):
        pass

    def visit_node_end(self, node: Node):
        pass

    def visit_leaf(self, node: Node):
        pass

    def visit_string(self, node: StringNode):
        pass
