from typing import Union

from contracts.nodes.Ast import Ast
from contracts.nodes.Forest import Forest
from contracts.nodes.MarkerNode import MarkerNode
from contracts.nodes.Node import Node
from contracts.nodes.PredicateNode import PredicateNode
from contracts.nodes.RootNode import RootNode
from contracts.nodes.StringNode import StringNode
from contracts.nodes.WordNode import WordNode
from contracts.visitors.AstVisitor import AstVisitor


class AstDfsVisitor:
    @property
    def depth(self):
        return self._depth

    def __init__(self):
        self._depth = 0

    def accept(self, visitable: Union[Forest, Ast, Node], visitor: AstVisitor):
        if self._depth == 0:
            visitor.visit()
        self._depth += 1
        if isinstance(visitable, Forest):
            for tree in visitable.trees:
                self.accept(tree.root, visitor)
        elif isinstance(visitable, Ast):
            self.accept(visitable.root, visitor)
        elif isinstance(visitable, RootNode):
            self._accept_root(visitable, visitor)
        elif isinstance(visitable, StringNode):
            self._accept_string(visitable, visitor)
        elif isinstance(visitable, WordNode):
            self._accept_word(visitable, visitor)
        elif isinstance(visitable, PredicateNode):
            self._accept_predicate(visitable, visitor)
        elif isinstance(visitable, MarkerNode):
            self._accept_marker(visitable, visitor)
        elif isinstance(visitable, Node):
            self._accept_node(visitable, visitor)
        else:
            raise ValueError("Argument of accept function is not visitable")
        self._depth -= 1
        if self._depth == 0:
            visitor.visit_end()

    def _accept_root(self, node: RootNode, visitor: AstVisitor):
        visitor.visit_root(node)
        self._accept_node(node, visitor)
        visitor.visit_root_end(node)

    def _accept_string(self, node: StringNode, visitor: AstVisitor):
        visitor.visit_string(node)
        self._accept_node(node, visitor)
        visitor.visit_string_end(node)

    def _accept_word(self, node: WordNode, visitor: AstVisitor):
        visitor.visit_word(node)
        self._accept_node(node, visitor)
        visitor.visit_word_end(node)

    def _accept_predicate(self, node: PredicateNode, visitor: AstVisitor):
        visitor.visit_predicate(node)
        self._accept_node(node, visitor)
        visitor.visit_predicate_end(node)

    def _accept_marker(self, node: MarkerNode, visitor: AstVisitor):
        visitor.visit_marker(node)
        self._accept_node(node, visitor)
        visitor.visit_marker_end(node)

    def _accept_node(self, node: Node, visitor: AstVisitor):
        visitor.visit_node(node)
        for child in node.children:
            self.accept(child, visitor)
        visitor.visit_node_end(node)
