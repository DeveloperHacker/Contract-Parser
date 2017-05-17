from abc import ABCMeta

from contract_parser.nodes.Node import Node
from contract_parser.nodes.RootNode import RootNode
from contract_parser.nodes.StringNode import StringNode
from contract_parser.nodes.Ast import Tree
from contract_parser.nodes.WordNode import WordNode


class TreeVisitor(metaclass=ABCMeta):
    @property
    def depth(self):
        return self._depth

    def __init__(self):
        self._depth: int = 0

    def accept(self, visitable):
        if self._depth == 0: self._visit()
        self._depth += 1
        if isinstance(visitable, Tree):
            self.accept_tree(visitable)
        elif isinstance(visitable, RootNode):
            self.accept_root_node(visitable)
        elif isinstance(visitable, StringNode):
            self.accept_string_node(visitable)
        elif isinstance(visitable, WordNode):
            self.accept_word_node(visitable)
        elif isinstance(visitable, Node):
            self.accept_other_node(visitable)
        else:
            raise ValueError("Argument of accept function is not visitable")
        self._depth -= 1
        if self._depth == 0: self._visit_end()

    def accept_tree(self, tree: Tree):
        self._visit_tree(tree)
        for root in tree.roots:
            self.accept(root)
        self._visit_tree_end(tree)

    def accept_root_node(self, node: RootNode):
        self._visit_root(node)
        self.accept_node(node)
        self._visit_root_end(node)

    def accept_string_node(self, node: StringNode):
        self._visit_string(node)
        self.accept_node(node)
        self._visit_string_end(node)

    def accept_word_node(self, node: WordNode):
        self._visit_word(node)
        self.accept_node(node)
        self._visit_word_end(node)

    def accept_other_node(self, node: Node):
        self._visit_other_node(node)
        self.accept_node(node)
        self._visit_other_node_end(node)

    def accept_node(self, node: Node):
        self._visit_node(node)
        for child in node.children:
            self.accept(child)
        self._visit_node_end(node)

    def _visit(self):
        pass

    def _visit_end(self):
        pass

    # Tree
    def _visit_tree(self, tree: Tree):
        pass

    def _visit_tree_end(self, tree: Tree):
        pass

    # Node
    def _visit_node(self, node: Node):
        pass

    def _visit_node_end(self, node: Node):
        pass

    # Other Node
    def _visit_other_node(self, node: Node):
        pass

    def _visit_other_node_end(self, node: Node):
        pass

    # Root
    def _visit_root(self, node: RootNode):
        pass

    def _visit_root_end(self, node: RootNode):
        pass

    # String
    def _visit_string(self, node: StringNode):
        pass

    def _visit_string_end(self, node: StringNode):
        pass

    # Word
    def _visit_word(self, node: WordNode):
        pass

    def _visit_word_end(self, node: WordNode):
        pass
