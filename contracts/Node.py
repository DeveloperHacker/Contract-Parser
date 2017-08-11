from contracts.Token import Token


class Node:
    def __init__(self, token: Token, *children: 'Node'):
        self.token = token
        self.children = list(children)

    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, Node):
            if len(self.children) != len(other.children):
                return False
            for child, other_child in zip(self.children, other.children):
                if child != other_child:
                    return False
            return self.token == other.token
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def leaf(self) -> bool:
        return len(self.children) == 0

    def __str__(self):
        children = ",".join(str(child) for child in self.children)
        name = self.token.name
        return name if self.leaf() else "%s(%s)" % (name, children)

    def height(self) -> int:
        if self.leaf():
            return 1
        return max(child.height() for child in self.children) + 1
