from typing import List

from contracts.BfsGuide import BfsGuide
from contracts.DfsGuide import DfsGuide
from contracts.Node import Node
from contracts.Token import Token
from contracts.Tree import Tree
from contracts.TreeVisitor import TreeGuide
from contracts.TreeVisitor import TreeVisitor


class Compiler(TreeVisitor):
    def __init__(self, guide: TreeGuide):
        super().__init__(guide)
        self.tokens = None

    def result(self) -> List[Token]:
        return self.tokens

    def visit_tree(self, tree: Tree):
        self.tokens = []

    def visit_node(self, depth: int, node: Node, parent: Node):
        self.tokens.append(node.token)


class DfsCompiler(Compiler):
    def __init__(self):
        super().__init__(DfsGuide())


class BfsCompiler(Compiler):
    def __init__(self):
        super().__init__(BfsGuide())
