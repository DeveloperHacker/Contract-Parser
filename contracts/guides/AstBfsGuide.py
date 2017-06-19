from contracts.guides.AstGuide import AstGuide
from contracts.nodes.Node import Node
from contracts.nodes.StringNode import StringNode


class AstBfsGuide(AstGuide):
    def _accept(self, visitable: Node):
        queue = [visitable]
        while len(queue) > 0:
            visitable = queue.pop(0)
            self._visitor.visit_node(visitable)
            if visitable.is_leaf():
                self._visitor.visit_leaf(visitable)
            if isinstance(visitable, StringNode):
                self._visitor.visit_string(visitable)
            self._visitor.visit_node_end(visitable)
            for child in visitable.children:
                queue.append(child)
