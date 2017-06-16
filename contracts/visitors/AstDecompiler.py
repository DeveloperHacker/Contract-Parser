from contracts.nodes.MarkerNode import MarkerNode
from contracts.nodes.Node import Node
from contracts.nodes.PredicateNode import PredicateNode
from contracts.nodes.RootNode import RootNode
from contracts.nodes.StringNode import StringNode
from contracts.nodes.WordNode import WordNode
from contracts.visitors.AstVisitor import AstVisitor


class AstDecompiler(AstVisitor):
    def __init__(self):
        super().__init__()
        self.tokens = None
        self.stack = None

    def visit(self):
        self.tokens = []
        self.stack = []

    def visit_node(self, node: Node):
        self.stack.append(self.tokens)
        self.tokens = []

    def visit_predicate_end(self, node: PredicateNode):
        string = "{}({})".format(node.token.name, ", ".join(self.tokens))
        self.tokens = self.stack.pop()
        self.tokens.append(string)

    def visit_marker_end(self, node: MarkerNode):
        self.tokens = self.stack.pop()
        self.tokens.append(node.token.name)

    def visit_root_end(self, node: RootNode):
        if len(self.tokens) != 1:
            raise ValueError("Root node have more single child. WTF?")
        string = "{} {}".format(node.token.name, self.tokens[0])
        self.tokens = self.stack.pop()
        self.tokens.append(string)

    def visit_string_end(self, node: StringNode):
        string = "\"" + " ".join(self.tokens) + "\""
        self.tokens = self.stack.pop()
        self.tokens.append(string)

    def visit_word_end(self, node: WordNode):
        if len(self.tokens) != 0:
            raise ValueError("Word node have children. WTF?")
        self.tokens = self.stack.pop()
        self.tokens.append(node.instance)

    def __str__(self) -> str:
        if self.tokens is None:
            raise ValueError()
        return "\n".join(self.tokens)
