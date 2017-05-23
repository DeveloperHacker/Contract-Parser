from contracts.nodes.Node import Node
from contracts.tokens.Token import Token


class RootNode(Node):
    def __init__(self, token: Token, child: Node = None):
        super().__init__(token, [child] if child else None)
