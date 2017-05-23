from contracts.nodes.Node import Node
from contracts.tokens.PredicateToken import PredicateToken


class PredicateNode(Node):
    def __init__(self, token: PredicateToken, children: Node = None):
        super().__init__(token, children)
