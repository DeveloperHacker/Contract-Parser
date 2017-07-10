from contracts.nodes.Ast import Ast

from contracts.nodes.Node import Node
from contracts.tokens import tokens
from contracts.visitors.AstVisitor import AstVisitor


class AstEqualReducer(AstVisitor):
    def __init__(self):
        self.ast = None

    def visit_end(self, ast: Ast):
        ast.root = AstEqualReducer.reduce(ast.root)
        self.ast = ast

    def visit_node_end(self, node: Node):
        children = []
        for child in node.children:
            child = AstEqualReducer.reduce(child)
            child.parent = node
            children.append(child)
        node.children = children

    @staticmethod
    def reduce(node: Node):
        if node.token == tokens.NOT_EQUAL:
            assert node.children is not None
            assert len(node.children) == 2
            left = node.children[0]
            right = node.children[1]
            if left.token == tokens.FALSE:
                node = right
            elif right.token == tokens.FALSE:
                node = left
            elif left.token == tokens.TRUE:
                node.token = tokens.EQUAL
                left.token = tokens.FALSE
                node.children = [right, left]
            elif right.token == tokens.TRUE:
                node.token = tokens.EQUAL
                right.token = tokens.FALSE
        if node.token == tokens.EQUAL:
            assert node.children is not None
            assert len(node.children) == 2
            left = node.children[0]
            right = node.children[1]
            if left.token == tokens.TRUE:
                node = right
            elif right.token == tokens.TRUE:
                node = left
            elif left.token == tokens.FALSE:
                node.children = [right, left]
        return node

    def result(self):
        return self.ast
