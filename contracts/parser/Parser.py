from typing import List, Dict

from contracts.nodes.Ast import Ast
from contracts.nodes.Node import Node
from contracts.nodes.StringNode import StringNode
from contracts.parser import grammar
from contracts.tokens import Tokens, Labels, Predicates, Markers, Operators
from contracts.tokens.LabelToken import LabelToken
from contracts.tokens.MarkerToken import MarkerToken
from contracts.tokens.OperatorToken import OperatorToken
from contracts.tokens.PredicateToken import PredicateToken
from contracts.tokens.StringToken import StringToken
from contracts.tokens.Token import Token


class ParseException(Exception):
    def __init__(self, message: str):
        super().__init__("AnalyseException: {}".format(message))


class UnexpectedTokenException(ParseException):
    def __init__(self, token: Token):
        super().__init__("token '{}' wasn't expected".format(token))


class UnexpectedEofException(ParseException):
    def __init__(self):
        super().__init__("unexpected the end of the contract")


class ExpectedEofException(ParseException):
    def __init__(self):
        super().__init__("expected the end of the contract")


class StringInstanceNotFoundException(ParseException):
    def __init__(self):
        super().__init__("instance of string hasn't found")


def parse_tree(label: LabelToken, tokens: List[Token], strings: Dict[int, List[str]], bypass: str = "dfs") -> Ast:
    if bypass == "dfs":
        return dfs_parse_tree(label, tokens, strings)
    if bypass == "bfs":
        return bfs_parse_tree(label, tokens, strings)
    raise ValueError("Collapse type hasn't recognize")


def dfs_parse_tree(label: LabelToken, tokens: List[Token], strings: Dict[int, List[str]]) -> Ast:
    def parse_token() -> Node:
        index, token = next(tail, (None, None))
        if token is None:
            raise UnexpectedEofException()
        if isinstance(token, StringToken):
            if index not in strings:
                raise StringInstanceNotFoundException()
            node = StringNode(strings[index])
        elif isinstance(token, PredicateToken):
            children = [parse_token() for _ in range(token.num_arguments)]
            node = Node(token, children)
        elif isinstance(token, MarkerToken):
            node = Node(token)
        else:
            raise UnexpectedTokenException(token)
        return node

    tail = enumerate(tokens)
    root = parse_token()
    if next(tail, None) is not None:
        raise ExpectedEofException()
    return Ast(label, root)


def bfs_parse_tree(label: LabelToken, tokens: List[Token], strings: Dict[int, List[str]]) -> Ast:
    def parse_token() -> (Node, List[Node]):
        token = tokens[idx]
        if isinstance(token, StringToken):
            if idx not in strings:
                raise StringInstanceNotFoundException()
            local_node = StringNode(strings[idx])
        elif isinstance(token, PredicateToken):
            local_node = Node(token)
            parents.extend([local_node] * token.num_arguments)
        elif isinstance(token, MarkerToken):
            local_node = Node(token)
        else:
            raise UnexpectedTokenException(token)
        return local_node

    if len(tokens) == 0:
        raise UnexpectedEofException()
    idx = 0
    parents = []
    root = parse_token()
    if isinstance(tokens[idx], PredicateToken):
        for idx in range(1, len(tokens)):
            parent = parents[idx - 1]
            node = parse_token()
            parent.children.append(node)
            node.parent = parent
    elif len(tokens) != 1:
        raise ExpectedEofException()
    return Ast(label, root)


def parse(code: str) -> List[Ast]:
    Tokens.register_all_tokens()
    forest = []
    stack = []

    def parse_operator(operator):
        operator = " ".join(operator)
        token = Operators.value_of(operator)
        assert isinstance(token, OperatorToken)
        token = token.predicate
        assert len(stack) >= token.num_arguments
        node = Node(token, stack[-token.num_arguments:])
        del stack[-token.num_arguments:]
        stack.append(node)

    def parse_marker(marker):
        marker = marker[0]
        token = Markers.value_of(marker)
        assert isinstance(token, MarkerToken)
        node = Node(token)
        stack.append(node)

    def parse_predicate(predicate):
        predicate = predicate[0]
        token = Predicates.value_of(predicate)
        assert isinstance(token, PredicateToken)
        assert len(stack) >= token.num_arguments
        node = Node(token, stack[-token.num_arguments:])
        del stack[-token.num_arguments:]
        stack.append(node)

    def parse_string(string):
        string = string[0]
        assert len(string) > 0
        if string[0] in ("\"", "'"):
            assert string[-1] == string[0]
            string = string[1:-1]
        node = StringNode(string.split(" "))
        stack.append(node)

    def parse_label(label):
        label = label[0]
        token = Labels.value_of(label)
        assert isinstance(token, LabelToken)
        assert len(stack) == 1
        ast = Ast(token, stack[0])
        forest.append(ast)
        del stack[0]

    parser = grammar.build(parse_operator, parse_marker, parse_predicate, parse_string, parse_label)
    parser.parseString(code)
    return forest
