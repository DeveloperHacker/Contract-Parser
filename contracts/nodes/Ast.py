from contracts.nodes.RootNode import RootNode


class Ast:
    def __init__(self, root: RootNode):
        self.root = root

    def __str__(self) -> str:
        return "\n".join(self.root.str(0))

    def consistent(self) -> bool:
        pass
