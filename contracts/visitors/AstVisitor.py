from abc import ABCMeta

from contracts.nodes.Ast import Ast
from contracts.nodes.MarkerNode import MarkerNode
from contracts.nodes.Node import Node
from contracts.nodes.PredicateNode import PredicateNode
from contracts.nodes.RootNode import RootNode
from contracts.nodes.StringNode import StringNode
from contracts.nodes.WordNode import WordNode


class AstVisitor(metaclass=ABCMeta):
    @property
    def depth(self):
        return self._depth

    def __init__(self):
        self._depth = 0

    def accept(self, visitable):
        if self._depth == 0: self._visit()
        self._depth += 1
        if isinstance(visitable, Ast):
            self._accept_tree(visitable)
        elif isinstance(visitable, RootNode):
            self._accept_root(visitable)
        elif isinstance(visitable, StringNode):
            self._accept_string(visitable)
        elif isinstance(visitable, WordNode):
            self._accept_word(visitable)
        elif isinstance(visitable, PredicateNode):
            self._accept_predicate(visitable)
        elif isinstance(visitable, MarkerNode):
            self._accept_marker(visitable)
        elif isinstance(visitable, Node):
            self._accept_node(visitable)
        else:
            raise ValueError("Argument of accept function is not visitable")
        self._depth -= 1
        if self._depth == 0: self._visit_end()

    def _accept_tree(self, tree: Ast):
        self._visit_tree(tree)
        for root in tree.roots:
            self.accept(root)
        self._visit_tree_end(tree)

    def _accept_root(self, node: RootNode):
        self._visit_root(node)
        self._accept_node(node)
        self._visit_root_end(node)

    def _accept_string(self, node: StringNode):
        self._visit_string(node)
        self._accept_node(node)
        self._visit_string_end(node)

    def _accept_word(self, node: WordNode):
        self._visit_word(node)
        self._accept_node(node)
        self._visit_word_end(node)

    def _accept_predicate(self, node: PredicateNode):
        self._visit_predicate(node)
        self._accept_node(node)
        self._visit_predicate_end(node)

    def _accept_marker(self, node: MarkerNode):
        self._visit_marker(node)
        self._accept_node(node)
        self._visit_marker_end(node)

    def _accept_node(self, node: Node):
        self._visit_node(node)
        for child in node.children:
            self.accept(child)
        self._visit_node_end(node)

    def _visit(self):
        pass

    def _visit_end(self):
        pass

    # Tree
    def _visit_tree(self, tree: Ast):
        pass

    def _visit_tree_end(self, tree: Ast):
        pass

    # Node
    def _visit_node(self, node: Node):
        pass

    def _visit_node_end(self, node: Node):
        pass

    # Function Node
    def _visit_predicate(self, node: PredicateNode):
        pass

    def _visit_predicate_end(self, node: PredicateNode):
        pass

    # Marker Node
    def _visit_marker(self, node: MarkerNode):
        pass

    def _visit_marker_end(self, node: MarkerNode):
        pass

    # Root Node
    def _visit_root(self, node: RootNode):
        pass

    def _visit_root_end(self, node: RootNode):
        pass

    # String Node
    def _visit_string(self, node: StringNode):
        pass

    def _visit_string_end(self, node: StringNode):
        pass

    # Word Node
    def _visit_word(self, node: WordNode):
        pass

    def _visit_word_end(self, node: WordNode):
        pass
