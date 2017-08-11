from queue import Queue

from contracts.Node import Node
from contracts.TreeVisitor import TreeGuide


class BfsGuide(TreeGuide):
    def accept(self, node: Node):
        super().accept(node)
        queue = Queue()
        queue.put((1, node, None))
        while not queue.empty():
            depth, node, parent = queue.get()
            self.visitor.visit(depth, node, parent)
            self.visitor.visit_end(depth, node, parent)
            for child in node.children:
                queue.put((depth + 1, child, node))
