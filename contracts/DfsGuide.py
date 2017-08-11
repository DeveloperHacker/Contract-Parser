from contracts.Node import Node

from contracts.TreeVisitor import TreeGuide


class DfsGuide(TreeGuide):
    def accept(self, node: Node):
        super().accept(node)
        self._accept(1, node, None)

    def _accept(self, depth: int, node: Node, parent: Node):
        self.visitor.visit(depth, node, parent)
        for child in node.children:
            self._accept(depth + 1, child, node)
        self.visitor.visit_end(depth, node, parent)
