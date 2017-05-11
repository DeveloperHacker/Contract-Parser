from parser.Node import Node
from parser.Token import Label


class Tree:
    def __init__(self, label: Label, root: Node):
        self.label = label
        self.root = root
