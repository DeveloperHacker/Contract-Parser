from abc import ABCMeta, abstractmethod

from contracts.nodes.Ast import Ast
from contracts.nodes.Node import Node
from contracts.visitors.AstVisitor import AstVisitor


class AstGuide(metaclass=ABCMeta):
    def __init__(self, visitor: AstVisitor):
        self._visitor = visitor

    def accept(self, ast: Ast):
        self._visitor.visit(ast)
        self._accept(ast.root)
        self._visitor.visit_end(ast)
        return self._visitor.result()

    @abstractmethod
    def _accept(self, visitable: Node):
        pass
