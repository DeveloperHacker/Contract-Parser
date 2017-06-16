from contracts.nodes.Ast import Ast
from contracts.nodes.MarkerNode import MarkerNode
from contracts.nodes.Node import Node
from contracts.nodes.PredicateNode import PredicateNode
from contracts.nodes.RootNode import RootNode
from contracts.nodes.StringNode import StringNode
from contracts.nodes.WordNode import WordNode
from contracts.visitors.AstVisitor import AstVisitor


class AstBfsVisitor:
    def accept(self, ast: Ast, visitor: AstVisitor):
        visitor.visit()
        queue = [ast.root]
        while len(queue) > 0:
            visitable = queue.pop(0)
            if isinstance(visitable, RootNode):
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
                raise ValueError("Tree is not consistent")
            for child in visitable.children:
                queue.append(child)

        visitor.visit_end()

    @staticmethod
    def _accept_root(node: RootNode, visitor: AstVisitor):
        visitor.visit_root(node)
        AstBfsVisitor._accept_node(node, visitor)
        visitor.visit_root_end(node)

    @staticmethod
    def _accept_string(node: StringNode, visitor: AstVisitor):
        visitor.visit_string(node)
        AstBfsVisitor._accept_node(node, visitor)
        visitor.visit_string_end(node)

    @staticmethod
    def _accept_word(node: WordNode, visitor: AstVisitor):
        visitor.visit_word(node)
        AstBfsVisitor._accept_node(node, visitor)
        visitor.visit_word_end(node)

    @staticmethod
    def _accept_predicate(node: PredicateNode, visitor: AstVisitor):
        visitor.visit_predicate(node)
        AstBfsVisitor._accept_node(node, visitor)
        visitor.visit_predicate_end(node)

    @staticmethod
    def _accept_marker(node: MarkerNode, visitor: AstVisitor):
        visitor.visit_marker(node)
        AstBfsVisitor._accept_node(node, visitor)
        visitor.visit_marker_end(node)

    @staticmethod
    def _accept_node(node: Node, visitor: AstVisitor):
        visitor.visit_node(node)
        visitor.visit_node_end(node)
