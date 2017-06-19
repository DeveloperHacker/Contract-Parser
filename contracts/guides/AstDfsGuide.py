from contracts.guides.AstGuide import AstGuide
from contracts.nodes.Node import Node
from contracts.nodes.StringNode import StringNode


class AstDfsGuide(AstGuide):
    def _accept(self, node: Node):
        self._visitor.visit_node(node)
        if node.is_leaf():
            self._visitor.visit_leaf(node)
        if isinstance(node, StringNode):
            self._visitor.visit_string(node)
        for child in node.children:
            self._accept(child)
        self._visitor.visit_node_end(node)
