from contracts.nodes.Node import Node
from contracts.tokens.MarkerToken import MarkerToken


class MarkerNode(Node):
    def __init__(self, token: MarkerToken):
        super().__init__(token)
