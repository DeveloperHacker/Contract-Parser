from enum import Enum

from typing import Iterable, Tuple

from src.parser.nodes.Node import Node
from src.parser.nodes.RootNode import RootNode
from src.parser.nodes.StringNode import StringNode
from src.parser.nodes.Tree import Tree
from src.parser.nodes.WordNode import WordNode
from src.parser.tokens import tokens
from src.parser.tokens.FunctionToken import FunctionToken
from src.parser.tokens.LabelToken import LabelToken
from src.parser.tokens.MarkerToken import MarkerToken
from src.parser.tokens.Token import Token


class Parser:
    class ParseException(Exception):
        def __init__(self, line: int, message: str):
            super().__init__("in {}: ParseError: {}".format(line, message))

    class StringNotClosedException(ParseException):
        def __init__(self, line: int):
            super().__init__(line, "string wasn't closed")

    class NotRecognizeException(ParseException):
        def __init__(self, line: int, token: str):
            super().__init__(line, "token '{}' hasn't been recognized".format(token))

    class UnexpectedTokenException(ParseException):
        def __init__(self, line: int, token: str):
            super().__init__(line, "token '{}' wasn't expected".format(token))

    class TooManyArgumentsException(ParseException):
        def __init__(self, line: int, token: FunctionToken, num_arguments: int):
            text = "too many arguments ib predicate '{}', expected {}, got {}" \
                .format(token.name, token.max_num_arguments, num_arguments)
            super().__init__(line, text)

    class TooFewArgumentsException(ParseException):
        def __init__(self, line: int, token: FunctionToken, num_arguments: int):
            text = "too few arguments ib predicate '{}', expected {}, got {}" \
                .format(token.name, token.min_num_arguments, num_arguments)
            super().__init__(line, text)

    @staticmethod
    def split(source: str) -> Iterable[str]:
        splited = []
        delimiters = ("(", ")", ",", " ", "\"", "\n")
        trash_symbols = (" ", ",", "\"", "\n")
        token = []
        start_string = None
        in_str = False
        prev = None
        line = 1
        for ch in source:
            if ch == "\"":
                if in_str and prev != "\\":
                    in_str = False
                elif not in_str:
                    in_str = True
                    start_string = line
            if not in_str and ch in delimiters:
                token = "".join(token).strip()
                if len(token) > 0:
                    splited.append((line, token))
                if ch not in trash_symbols:
                    splited.append((line, ch))
                token = []
            else:
                token.append(ch)
            prev = None if in_str and prev == "\\" else ch
            if ch == "\n":
                line += 1
        if in_str:
            raise Parser.StringNotClosedException(start_string)
        token = "".join(token).strip()
        if len(token) > 0:
            splited.append((line, token))
        return splited

    @staticmethod
    def is_string(token: str):
        return len(token) > 0 and token[0] == "\""

    @staticmethod
    def parse(source: str) -> Iterable[Tuple[Token, str]]:
        class State(Enum):
            LABEL = 0
            ARGUMENT = 1
            INVOKE = 2

        parsed = []
        stack = []
        num_arguments = 0
        state = State.LABEL
        for line, element in Parser.split(source):
            if state == State.LABEL:
                if Parser.is_string(element):
                    raise Parser.UnexpectedTokenException(line, element)
                if not Token.is_token(element):
                    raise Parser.NotRecognizeException(line, element)
                token = Token.value_of(element)
                if isinstance(token, LabelToken):
                    parsed.append((token, None))
                    state = State.ARGUMENT
                elif isinstance(token, FunctionToken):
                    stack.append((token, num_arguments))
                    parsed.append((tokens.UNDEFINED, None))
                    parsed.append((token, None))
                    state = State.INVOKE
                else:
                    raise Parser.UnexpectedTokenException(line, element)
            elif state == State.INVOKE:
                if Parser.is_string(element):
                    raise Parser.UnexpectedTokenException(line, element)
                if not Token.is_token(element):
                    raise Parser.NotRecognizeException(line, element)
                token = Token.value_of(element)
                if token != tokens.LB:
                    raise Parser.UnexpectedTokenException(line, element)
                state = State.ARGUMENT
                num_arguments = 0
            elif state == State.ARGUMENT:
                if Parser.is_string(element):
                    for word in element[1:].split(" "):
                        parsed.append((tokens.WORD, word))
                    parsed.append((tokens.END_STRING, None))
                    num_arguments += 1
                elif Token.is_token(element):
                    token = Token.value_of(element)
                    if token == tokens.RB:
                        if len(stack) == 0:
                            raise Parser.UnexpectedTokenException(line, element)
                        token, _num_arguments = stack.pop()
                        if token.max_num_arguments > num_arguments:
                            raise Parser.TooManyArgumentsException(line, token, num_arguments)
                        if token.min_num_arguments < num_arguments:
                            raise Parser.TooFewArgumentsException(line, token, num_arguments)
                        parsed.append((tokens.END_ARGS, None))
                        num_arguments = _num_arguments
                        if len(stack) == 0:
                            state = State.LABEL
                    elif isinstance(token, FunctionToken):
                        num_arguments += 1
                        stack.append((token, num_arguments))
                        parsed.append((token, None))
                        state = State.INVOKE
                    elif isinstance(token, MarkerToken):
                        parsed.append((token, None))
                        num_arguments += 1
                    else:
                        raise Parser.UnexpectedTokenException(line, element)
                else:
                    raise Parser.NotRecognizeException(line, element)
        return parsed

    @staticmethod
    def tree(parsed: Iterable[Tuple[Token, str]]) -> Tree:
        class State(Enum):
            LABEL = 0
            ARGUMENT = 1
            STRING = 2

        tree = Tree()
        node = None
        stack = []
        state = State.LABEL
        for token, word in parsed:
            if state == State.LABEL:
                node = RootNode(token)
                tree.roots.append(node)
                state = State.ARGUMENT
            elif state == State.ARGUMENT:
                if token == tokens.END_ARGS:
                    node = stack.pop()
                    if len(stack) == 0:
                        state = State.LABEL
                elif token == tokens.WORD:
                    stack.append(node)
                    _node = StringNode(tokens.STRING)
                    node.children.append(_node)
                    node = _node
                    node.children.append(WordNode(word))
                    state = State.STRING
                elif isinstance(token, FunctionToken):
                    stack.append(node)
                    _node = Node(token)
                    node.children.append(_node)
                    node = _node
                else:
                    node.children.append(Node(token))
            elif state == State.STRING:
                if token == tokens.END_STRING:
                    node = stack.pop()
                    state = State.ARGUMENT
                else:
                    node.children.append(WordNode(word))
        return tree
