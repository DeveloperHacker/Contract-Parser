import re
from typing import Iterable, List

from contracts import Types, Tokens
from contracts.Node import Node
from contracts.Token import Token
from contracts.Tree import Tree


def typing(raw_tokens: Iterable[str]) -> Iterable[Token]:
    def get_type() -> str:
        if len(raw_token) > 1 and raw_token[0] in ('"', "'") and raw_token[0] == raw_token[-1]:
            return Types.STRING
        matches = re.match(r"%s\[(0|[1-9][0-9]*)\]" % Tokens.PARAM, raw_token)
        if matches:
            return Types.MARKER
        try:
            index = {name == raw_token: type for type, names in Tokens.instances.items() for name in names}
            return index[True]
        except KeyError:
            raise ValueError("Token with name '%s' can't be identified" % raw_token)

    for raw_token in raw_tokens:
        yield Token(raw_token, get_type())


def dfs(tokens: Iterable[Token]) -> Tree:
    def parse_token(token: Token) -> Node:
        if token.type == Types.OPERATOR:
            left = parse_token(next(tail))
            right = parse_token(next(tail))
            node = Node(token, left, right)
        elif token.type == Types.ROOT:
            children = []
            child_token = next(tail, None)
            while child_token is not None:
                child = parse_token(child_token)
                children.append(child)
                child_token = next(tail, None)
            node = Node(token, *children)
        elif token.type in Types.MARKER:
            node = Node(token)
        elif token.type == Types.STRING:
            node = Node(token)
        elif token.type == Types.LABEL:
            node = Node(token, parse_token(next(tail)))
        else:
            raise Exception("Unexpected Type of token with name '%s'" % token.type)
        return node

    try:
        tail = iter(tokens)
        root = parse_token(next(tail))
    except StopIteration:
        raise Exception("Unexpected End of token stream")
    try:
        next(tail)
        raise Exception("Expected End of token stream")
    except StopIteration:
        tree = Tree(root)
    return tree


def bfs(tokens: Iterable[Token]) -> Tree:
    def parse_token(token: Token) -> (Node, List[Node]):
        if token.type == Types.OPERATOR:
            local_node = Node(token)
            parents.append(local_node)
            parents.append(local_node)
        elif token.type in Types.MARKER:
            local_node = Node(token)
        elif token.type == Types.STRING:
            local_node = Node(token)
        elif token.type == Types.LABEL:
            local_node = Node(token)
            parents.append(local_node)
        elif token.type == Types.ROOT:
            local_node = Node(token)
            num_labels = [token.type == Types.LABEL for token in tokens].count(True)
            parents.extend([local_node] * num_labels)
        else:
            raise Exception("Unexpected Type of token with name '%s'" % token.type)
        return local_node

    try:
        parents = []
        tokens = list(tokens)
        root = parse_token(tokens[0])
        for idx in range(1, len(tokens)):
            parent = parents[idx - 1]
            node = parse_token(tokens[idx])
            parent.children.append(node)
            node.parent = parent
        tree = Tree(root)
    except StopIteration:
        raise Exception("Unexpected End of token stream")
    except IndexError:
        raise Exception("Expected End of token stream")
    return tree
