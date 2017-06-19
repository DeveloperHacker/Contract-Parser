from contracts.nodes.Node import Node
from contracts.tokens.LabelToken import LabelToken


class Ast:
    def __init__(self, label: LabelToken, root: Node):
        self.label = label
        self.root = root

    def __str__(self) -> str:
        result = [self.label.name]
        result.extend(self.root.str(1))
        return "\n".join(result)

    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, Ast):
            return self.label.name == other.label.name and self.root == other.root
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    # noinspection PyMethodMayBeStatic
    def consistent(self) -> bool:
        return True
