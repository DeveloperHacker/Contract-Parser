from queue import Queue

from contracts.Node import Node


class Tree:
    def __init__(self, root: Node):
        self.root = root

    def __str__(self) -> str:
        return str(self.root)

    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, Tree):
            return self.root == other.root
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def string(self) -> str:
        return string(0, self.root)

    def height(self) -> int:
        return self.root.height()

    def clone(self) -> 'Tree':
        return Tree(self.root.clone())


def string(depth: int, node: Node) -> str:
    result = ["│" * depth + node.token.name]
    result.extend(string(depth + 1, node) for node in node.children)
    return "\n".join(result)
