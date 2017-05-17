from enum import Enum

from typing import List, Tuple

from contracts.nodes.Ast import Ast
from contracts.nodes.Node import Node
from contracts.nodes.RootNode import RootNode
from contracts.nodes.StringNode import StringNode
from contracts.nodes.WordNode import WordNode
from contracts.parser.Instruction import Instruction
from contracts.tokens import tokens
from contracts.tokens.FunctionToken import FunctionToken
from contracts.tokens.LabelToken import LabelToken
from contracts.tokens.MarkerToken import MarkerToken
from contracts.tokens.Token import Token


class Parser:
    class ParseException(Exception):
        def __init__(self, line: int, message: str):
            super().__init__("in {}: ParseException: {}".format(line, message))

    class AnalyseException(Exception):
        def __init__(self, message: str):
            super().__init__("AnalyseException: {}".format(message))

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

    class UnexpectedInstructionException(AnalyseException):
        def __init__(self, instruction: Instruction):
            super().__init__("instruction '{}' wasn't expected".format(instruction))

    class ExpectedEndInstructionException(AnalyseException):
        def __init__(self):
            super().__init__("expected instruction 'END' at the end of the contract")

    @staticmethod
    def split(source: str) -> List[str]:
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
    def parse(source: str) -> List[Instruction]:
        class State(Enum):
            LABEL = 0
            ARGUMENT = 1
            INVOKE = 2

        instructions: List[Instruction] = []
        stack: List[Tuple[FunctionToken, int]] = []
        num_arguments: int = 0
        state: State = State.LABEL
        for line, element in Parser.split(source):
            if state == State.LABEL:
                if Parser.is_string(element):
                    raise Parser.UnexpectedTokenException(line, element)
                if not Token.is_token(element):
                    raise Parser.NotRecognizeException(line, element)
                token = Token.value_of(element)
                if isinstance(token, LabelToken):
                    instructions.append(Instruction(token))
                    state = State.ARGUMENT
                elif isinstance(token, FunctionToken):
                    stack.append((token, num_arguments))
                    instructions.append(Instruction(tokens.UNDEFINED))
                    instructions.append(Instruction(token))
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
                        instructions.append(Instruction(tokens.WORD, word))
                    instructions.append(Instruction(tokens.END_STRING))
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
                        instructions.append(Instruction(tokens.END_ARGS))
                        num_arguments = _num_arguments
                        if len(stack) == 0:
                            state = State.LABEL
                    elif isinstance(token, FunctionToken):
                        num_arguments += 1
                        stack.append((token, num_arguments))
                        instructions.append(Instruction(token))
                        state = State.INVOKE
                    elif isinstance(token, MarkerToken):
                        instructions.append(Instruction(token))
                        num_arguments += 1
                    else:
                        raise Parser.UnexpectedTokenException(line, element)
                else:
                    raise Parser.NotRecognizeException(line, element)
        instructions.append(Instruction(tokens.END))
        return instructions

    @staticmethod
    def tree(instructions: List[Instruction]) -> Ast:
        class State(Enum):
            LABEL = 0
            ARGUMENT = 1
            STRING = 2
            END = 3

        tree: Ast = Ast()
        node: Node = None
        stack: List[Node] = []
        state: State = State.LABEL
        for instruction in instructions:
            if state == State.LABEL:
                if instruction.token == tokens.END:
                    state = State.END
                else:
                    node = RootNode(instruction.token)
                    tree.roots.append(node)
                    state = State.ARGUMENT
            elif state == State.ARGUMENT:
                if instruction.token == tokens.END_ARGS:
                    node = stack.pop()
                    if len(stack) == 0:
                        state = State.LABEL
                elif instruction.token == tokens.WORD:
                    stack.append(node)
                    _node = StringNode(tokens.STRING)
                    node.children.append(_node)
                    node = _node
                    node.children.append(WordNode(instruction.word))
                    state = State.STRING
                elif isinstance(instruction.token, FunctionToken):
                    stack.append(node)
                    _node = Node(instruction.token)
                    node.children.append(_node)
                    node = _node
                else:
                    node.children.append(Node(instruction.token))
            elif state == State.STRING:
                if instruction.token == tokens.END_STRING:
                    node = stack.pop()
                    state = State.ARGUMENT
                else:
                    node.children.append(WordNode(instruction.word))
            elif state == State.END:
                raise Parser.UnexpectedInstructionException(instruction)
        if state != State.END:
            raise Parser.ExpectedEndInstructionException()
        return tree
