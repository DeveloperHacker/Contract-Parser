from typing import List

from pyparsing import *

from contracts.Node import Node
from contracts.Token import Token
from contracts.Tokens import *
from contracts.Tokens import _THIS
from contracts.Tree import Tree
from contracts.Types import *
from contracts.Validator import Validator

FUNCTION = "function"
INVOCATION = "()"
SHORT_WEAK = "`"
GET = "get"


def build(parsers: dict):
    comma = Literal(",")
    rb = Literal(")")
    lb = Literal("(")
    srb = Literal("]")
    slb = Literal("[")
    number = Regex(r"0|[1-9][0-9]*")
    string = quotedString()
    name = Word(alphanums)
    label = Keyword(STRONG) | Keyword(WEAK) | Literal(SHORT_WEAK)
    marker = Keyword(RESULT) | Keyword(TRUE) | Keyword(FALSE) | Keyword(THIS) | Keyword(_THIS)
    function = Keyword(GET)
    get = Literal(GETATTR)
    contain = Literal(CONTAIN_PROPERTY) | Literal(NOT_CONTAIN_PROPERTY)
    operator2 = Literal(EQUAL) | Literal(NOT_EQUAL) | Keyword(MAY)
    operator2 |= And(Keyword(word) for word in IS_NOT.split(" ")) | Keyword(IS)
    operator2 |= Literal(GREATER_OR_EQUAL) | Literal(GREATER) | Literal(LOWER_OR_EQUAL) | Literal(LOWER)
    operator3 = Keyword(AND)
    operator4 = Keyword(OR)
    operator5 = Keyword(FOLLOW)

    expression = Forward()
    string_st = string.setParseAction(parsers[STRING])
    name_st = name.setParseAction(parsers[STRING])
    tuple_st = (expression + ZeroOrMore(comma + expression)) | Optional(expression)
    round_invocation_st = (lb + tuple_st + rb).setParseAction(parsers[INVOCATION])
    marker_st = (marker | Combine(Keyword(PARAM) + slb + number + srb)).setParseAction(parsers[MARKER])
    function_st = (function + Suppress(round_invocation_st)).setParseAction(parsers[FUNCTION])
    getattr_st = marker_st + ZeroOrMore((get + Suppress(name_st)).setParseAction(parsers[OPERATOR]))
    contain_st = getattr_st + ZeroOrMore((contain + Suppress(string_st)).setParseAction(parsers[OPERATOR]))
    atom_st = (lb + expression + rb) | function_st | string_st | contain_st
    operator_st = atom_st + ZeroOrMore((operator2 + Suppress(atom_st)).setParseAction(parsers[OPERATOR]))
    operator_st = operator_st + ZeroOrMore((operator3 + Suppress(operator_st)).setParseAction(parsers[OPERATOR]))
    operator_st = operator_st + ZeroOrMore((operator4 + Suppress(operator_st)).setParseAction(parsers[OPERATOR]))
    operator_st = operator_st + ZeroOrMore((operator5 + Suppress(operator_st)).setParseAction(parsers[OPERATOR]))
    expression << operator_st

    statement = (Optional(label, STRONG) + Suppress(expression)).setParseAction(parsers[LABEL])
    return ZeroOrMore(statement) + StringEnd()


def parse(code: str) -> Tree:
    def parse_label(strings: list):
        assert len(strings) == 1
        assert len(stack) == 1
        name = strings[0]
        if name == SHORT_WEAK:
            name = WEAK
        token = Token(name, LABEL)
        node = Node(token, stack.pop())
        tree.root.children.append(node)

    def parse_function(strings: list):
        assert len(strings) == 1
        assert len(stack) > 0
        assert stack[-1].token.name == INVOCATION
        assert stack[-1].token.type == INVOCATION
        assert len(stack[-1].children) == 2
        assert strings[0] == GET
        token = Token(GETATTR, OPERATOR)
        node = Node(token, *stack.pop().children)
        stack.append(node)

    def parse_operator(strings: list):
        assert len(stack) > 1
        name = " ".join(strings)
        token = Token(name, OPERATOR)
        right = stack.pop()
        left = stack.pop()
        node = Node(token, left, right)
        stack.append(node)

    def parse_marker(strings: list):
        assert len(strings) == 1
        name = strings[0]
        token = Token(name, MARKER)
        node = Node(token)
        stack.append(node)

    def parse_string(strings: list):
        assert len(strings) == 1
        name = strings[0]
        if name[0] not in ('"', "'"):
            name = "'" + name + "'"
        token = Token(name, STRING)
        node = Node(token)
        stack.append(node)

    def parse_invocation(strings: list):
        assert len(strings) > 1
        num_arguments = min(len(strings) - 2, list(strings).count(",") + 1)
        assert len(stack) >= num_arguments
        name = strings[0] + strings[-1]
        token = Token(name, INVOCATION)
        node = Node(token, *stack[-num_arguments:])
        del stack[-num_arguments:]
        stack.append(node)

    stack: List[Node] = []
    root_token = Token(ROOT, ROOT)
    root_node = Node(root_token)
    tree = Tree(root_node)
    parsers = {LABEL: parse_label,
               FUNCTION: parse_function,
               OPERATOR: parse_operator,
               MARKER: parse_marker,
               STRING: parse_string,
               INVOCATION: parse_invocation}
    parser = build(parsers)
    parser.parseString(code)
    assert len(stack) == 0
    Validator().accept(tree)
    return tree
