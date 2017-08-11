import re

from contracts import Types, Tokens
from contracts.DfsGuide import DfsGuide
from contracts.Node import Node
from contracts.TreeVisitor import TreeVisitor


def is_param(name: str) -> bool:
    matches = re.match(r"%s\[(0|[1-9][0-9]*)\]" % Tokens.PARAM, name)
    return matches is not None


class Validator(TreeVisitor):
    class ValidationException(Exception):
        def __init__(self, message: str):
            super().__init__(message)

    def __init__(self):
        super().__init__(DfsGuide())

    def visit_node(self, depth: int, node: Node, parent: Node):
        if node.token.type not in Types.instances:
            raise Validator.ValidationException("Token with type '%s' isn't supported" % node.token.type)

    def visit_root(self, depth: int, node: Node, parent: Node):
        if node.token.name != Tokens.ROOT:
            raise Validator.ValidationException("Token of tree root must have name '%s'" % Tokens.ROOT)
        if depth != 1:
            raise Validator.ValidationException("Token '%s' must be in root of tree" % Tokens.ROOT)
        if any(child.token.type != Types.LABEL for child in node.children):
            raise Validator.ValidationException("Token with type '%s' must be in after root of tree" % Types.LABEL)

    def visit_operator(self, depth: int, node: Node, parent: Node):
        if len(node.children) != 2:
            raise Validator.ValidationException("Number of Operator arguments must be equal 2")
        if node.token.name not in Tokens.instances[Types.OPERATOR]:
            raise Validator.ValidationException("Operator with name '%s' isn't supported" % node.token.name)

    def visit_marker(self, depth: int, node: Node, parent: Node):
        if not is_param(node.token.name) and node.token.name not in Tokens.instances[Types.MARKER]:
            raise Validator.ValidationException("Marker with name '%s' isn't supported" % node.token.name)

    def visit_string(self, depth: int, node: Node, parent: Node):
        name = node.token.name
        if len(name) < 2 or name[0] not in ("'", '"') or name[0] != name[-1]:
            raise Validator.ValidationException("String instance must be quoted")

    def visit_label(self, depth: int, node: Node, parent: Node):
        if node.token.name not in Tokens.instances[Types.LABEL]:
            raise Validator.ValidationException("Label with name '%s' isn't supported" % node.token.name)
        if parent is None or parent.token.type != Tokens.ROOT:
            raise Validator.ValidationException("Token '%s must be in after root of tree" % node.token.name)
