from abc import ABCMeta

from contracts.nodes.Forest import Forest
from contracts.nodes.MarkerNode import MarkerNode
from contracts.nodes.Node import Node
from contracts.nodes.PredicateNode import PredicateNode
from contracts.nodes.RootNode import RootNode
from contracts.nodes.StringNode import StringNode
from contracts.nodes.WordNode import WordNode


class AstVisitor(metaclass=ABCMeta):
    def visit(self):
        pass

    def visit_end(self):
        pass

    # Node
    def visit_node(self, node: Node):
        pass

    def visit_node_end(self, node: Node):
        pass

    # Function Node
    def visit_predicate(self, node: PredicateNode):
        pass

    def visit_predicate_end(self, node: PredicateNode):
        pass

    # Marker Node
    def visit_marker(self, node: MarkerNode):
        pass

    def visit_marker_end(self, node: MarkerNode):
        pass

    # Root Node
    def visit_root(self, node: RootNode):
        pass

    def visit_root_end(self, node: RootNode):
        pass

    # String Node
    def visit_string(self, node: StringNode):
        pass

    def visit_string_end(self, node: StringNode):
        pass

    # Word Node
    def visit_word(self, node: WordNode):
        pass

    def visit_word_end(self, node: WordNode):
        pass
