from enum import Enum

from typing import List, Tuple, Iterator

from contracts.nodes.Ast import Ast
from contracts.nodes.MarkerNode import MarkerNode
from contracts.nodes.Node import Node
from contracts.nodes.PredicateNode import PredicateNode
from contracts.nodes.RootNode import RootNode
from contracts.nodes.StringNode import StringNode
from contracts.nodes.WordNode import WordNode
from contracts.parser.Instruction import Instruction
from contracts.tokens import tokens
from contracts.tokens.LabelToken import LabelToken
from contracts.tokens.MarkerToken import MarkerToken
from contracts.tokens.PredicateToken import PredicateToken


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
        def __init__(self, line: int, token: PredicateToken, num_arguments: int):
            text = "too many arguments in predicate '{}', expected {}, got {}" \
                .format(token.name, token.num_arguments, num_arguments)
            super().__init__(line, text)

    class TooFewArgumentsException(ParseException):
        def __init__(self, line: int, token: PredicateToken, num_arguments: int):
            text = "too few arguments in predicate '{}', expected {}, got {}" \
                .format(token.name, token.num_arguments, num_arguments)
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
        stack: List[Tuple[PredicateToken, int]] = []
        num_arguments: int = 0
        state: State = State.LABEL
        for line, element in Parser.split(source):
            if state == State.LABEL:
                if Parser.is_string(element):
                    raise Parser.UnexpectedTokenException(line, element)
                if not tokens.is_token(element):
                    raise Parser.NotRecognizeException(line, element)
                token = tokens.value_of(element)
                if isinstance(token, LabelToken):
                    instructions.append(Instruction(token))
                    state = State.ARGUMENT
                else:
                    raise Parser.UnexpectedTokenException(line, element)
            elif state == State.INVOKE:
                if element != tokens.LB:
                    raise Parser.UnexpectedTokenException(line, element)
                state = State.ARGUMENT
                num_arguments = 0
            elif state == State.ARGUMENT:
                if Parser.is_string(element):
                    instructions.append(Instruction(tokens.STRING))
                    for word in element[1:].split(" "):
                        instructions.append(Instruction(tokens.WORD, word))
                    num_arguments += 1
                elif element == tokens.RB:
                    if len(stack) == 0:
                        raise Parser.UnexpectedTokenException(line, element)
                    token, _num_arguments = stack.pop()
                    if num_arguments > token.num_arguments:
                        raise Parser.TooManyArgumentsException(line, token, num_arguments)
                    if token.num_arguments > num_arguments:
                        raise Parser.TooFewArgumentsException(line, token, num_arguments)
                    num_arguments = _num_arguments
                    if len(stack) == 0:
                        state = State.LABEL
                elif tokens.is_token(element):
                    token = tokens.value_of(element)
                    if isinstance(token, PredicateToken):
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
    def parse_arguments(token: PredicateToken, tail: Iterator[Instruction]) -> (List[Node], Instruction):
        result = []
        instruction = next(tail, None)
        while instruction is not None:
            if len(result) == token.num_arguments:
                return result, instruction
            if instruction.token == tokens.STRING:
                node = StringNode()
                node.children, instruction = Parser.parse_string(tail)
                result.append(node)
            elif isinstance(instruction.token, PredicateToken):
                node = PredicateNode(instruction.token)
                node.children, instruction = Parser.parse_arguments(instruction.token, tail)
                result.append(node)
            elif isinstance(instruction.token, MarkerToken):
                node = MarkerNode(instruction.token)
                instruction = next(tail, None)
                result.append(node)
            else:
                raise Parser.UnexpectedInstructionException(instruction)
        for node in result:
            print(node.str(0))
        raise Parser.ExpectedEndInstructionException()

    @staticmethod
    def parse_string(tail: Iterator[Instruction]) -> (List[WordNode], Instruction):
        result = []
        instruction = next(tail, None)
        while instruction is not None:
            if instruction.token != tokens.WORD:
                return result, instruction
            result.append(WordNode(instruction.word))
            instruction = next(tail, None)
        raise Parser.ExpectedEndInstructionException()

    @staticmethod
    def tree(instructions: List[Instruction]) -> Ast:
        tree = Ast()
        tail = (instruction for instruction in instructions)
        instruction = next(tail, None)
        while instruction is not None:
            if instruction.token == tokens.END:
                break
            if isinstance(instruction.token, LabelToken):
                root = RootNode(instruction.token)
                instruction = next(tail, None)
                tree.roots.append(root)
                if isinstance(instruction.token, PredicateToken):
                    node = PredicateNode(instruction.token)
                    node.children, instruction = Parser.parse_arguments(instruction.token, tail)
                    root.children.append(node)
                else:
                    raise Parser.UnexpectedInstructionException(instruction)
            else:
                raise Parser.UnexpectedInstructionException(instruction)
        if instruction is None:
            raise Parser.ExpectedEndInstructionException()
        return tree
