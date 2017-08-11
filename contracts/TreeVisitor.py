from abc import ABCMeta, abstractmethod

from contracts.Node import Node
from contracts.Tree import Tree
from contracts.Types import *


class TreeGuide(metaclass=ABCMeta):
    def __init__(self):
        self.visitor = None

    @abstractmethod
    def accept(self, visitable: Node):
        pass


class TreeVisitor(metaclass=ABCMeta):
    def __init__(self, guide: TreeGuide):
        self.guide = guide
        self.visit_functions = {
            OPERATOR: (self.visit_operator, self.visit_operator_end),
            MARKER: (self.visit_marker, self.visit_marker_end),
            STRING: (self.visit_string, self.visit_string_end),
            LABEL: (self.visit_label, self.visit_label_end),
            ROOT: (self.visit_root, self.visit_root_end)
        }
        self.parents = {}

    def accept(self, tree: Tree):
        self.guide.visitor = self
        self.visit_tree(tree)
        self.guide.accept(tree.root)
        self.visit_tree_end(tree)
        self.guide.visitor = None
        return self.result()

    def visit(self, depth: int, node: Node, parent: Node):
        self.visit_node(depth, node, parent)
        if node.token.type in self.visit_functions:
            self.visit_functions[node.token.type][0](depth, node, parent)

    def visit_end(self, depth: int, node: Node, parent: Node):
        self.visit_node_end(depth, node, parent)
        if node.token.type in self.visit_functions:
            self.visit_functions[node.token.type][1](depth, node, parent)

    def result(self):
        pass

    def visit_tree(self, tree: Tree):
        pass

    def visit_tree_end(self, tree: Tree):
        pass

    def visit_node(self, depth: int, node: Node, parent: Node):
        pass

    def visit_node_end(self, depth: int, node: Node, parent: Node):
        pass

    def visit_root(self, depth: int, node: Node, parent: Node):
        pass

    def visit_root_end(self, depth: int, node: Node, parent: Node):
        pass

    def visit_operator(self, depth: int, node: Node, parent: Node):
        pass

    def visit_operator_end(self, depth: int, node: Node, parent: Node):
        pass

    def visit_marker(self, depth: int, node: Node, parent: Node):
        pass

    def visit_marker_end(self, depth: int, node: Node, parent: Node):
        pass

    def visit_string(self, depth: int, node: Node, parent: Node):
        pass

    def visit_string_end(self, depth: int, node: Node, parent: Node):
        pass

    def visit_label(self, depth: int, node: Node, parent: Node):
        pass

    def visit_label_end(self, depth: int, node: Node, parent: Node):
        pass
