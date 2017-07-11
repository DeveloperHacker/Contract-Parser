from enum import Enum
from typing import List, Tuple, Iterator, Dict

from contracts.nodes.Ast import Ast
from contracts.nodes.Node import Node
from contracts.nodes.StringNode import StringNode
from contracts.parser import grammar
from contracts.parser.Instruction import Instruction
from contracts.tokens import tokens
from contracts.tokens.LabelToken import LabelToken
from contracts.tokens.MarkerToken import MarkerToken
from contracts.tokens.OperatorToken import OperatorToken
from contracts.tokens.PredicateToken import PredicateToken
from contracts.tokens.StringToken import StringToken


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


class UnexpectedEofException(AnalyseException):
    def __init__(self):
        super().__init__("unexpected the end of the contract")


class ExpectedEofException(AnalyseException):
    def __init__(self):
        super().__init__("expected the end of the contract")


class StringInstanceNotFoundException(AnalyseException):
    def __init__(self):
        super().__init__("instance of string hasn't found")


quotes = ("\"", "'")


# def split(source: str) -> List[str]:
#     delimiters = ("(", ")", ",", " ", "\n")
#     trash_symbols = (" ", ",", "\n")
#
#     splited = []
#     token = []
#     start_string = None
#     in_str = False
#     open_quote = None
#     prev = None
#     line = 1
#     for ch in source:
#         if ch in quotes:
#             if in_str and prev != "\\" and ch == open_quote:
#                 in_str = False
#                 open_quote = None
#             elif not in_str:
#                 in_str = True
#                 open_quote = ch
#                 start_string = line
#         if not in_str and ch in (delimiters + quotes):
#             token = "".join(token).strip()
#             if len(token) > 0:
#                 splited.append((line, token))
#             if ch not in (trash_symbols + quotes):
#                 splited.append((line, ch))
#             token = []
#         else:
#             token.append(ch)
#         prev = None if in_str and prev == "\\" else ch
#         if ch == "\n":
#             line += 1
#     if in_str:
#         raise StringNotClosedException(start_string)
#     token = "".join(token).strip()
#     if len(token) > 0:
#         splited.append((line, token))
#     return splited
#
#
# def parse(source: str) -> (List[Tuple[LabelToken, List[Instruction], Dict[int, List[str]]]]):
#     class State(Enum):
#         LABEL = 0
#         ARGUMENT = 1
#         INVOKE = 2
#
#     def is_string(_token: str):
#         return len(_token) > 0 and _token[0] in quotes
#
#     strings: List[Dict[int, List[str]]] = []
#     instructions: List[List[Instruction]] = []
#     labels: List[LabelToken] = []
#     stack: List[Tuple[PredicateToken, int]] = []
#     num_arguments: int = 0
#     state: State = State.LABEL
#     for line, element in split(source):
#         if state == State.LABEL:
#             if is_string(element):
#                 raise UnexpectedTokenException(line, element)
#             if not tokens.is_token(element):
#                 raise NotRecognizeException(line, element)
#             token = tokens.value_of(element)
#             if isinstance(token, LabelToken):
#                 instructions.append([])
#                 strings.append({})
#                 labels.append(token)
#                 state = State.ARGUMENT
#             else:
#                 raise UnexpectedTokenException(line, element)
#         elif state == State.INVOKE:
#             if element != tokens.LB:
#                 raise UnexpectedTokenException(line, element)
#             state = State.ARGUMENT
#             num_arguments = 0
#         elif state == State.ARGUMENT:
#             if is_string(element):
#                 instructions[-1].append(Instruction(tokens.STRING))
#                 strings[-1][len(instructions[-1]) - 1] = element[1:].split(" ")
#                 num_arguments += 1
#             elif element == tokens.RB:
#                 if len(stack) == 0:
#                     raise UnexpectedTokenException(line, element)
#                 token, _num_arguments = stack.pop()
#                 if num_arguments > token.num_arguments:
#                     raise TooManyArgumentsException(line, token, num_arguments)
#                 if token.num_arguments > num_arguments:
#                     raise TooFewArgumentsException(line, token, num_arguments)
#                 num_arguments = _num_arguments
#                 if len(stack) == 0:
#                     state = State.LABEL
#             elif tokens.is_token(element):
#                 token = tokens.value_of(element)
#                 if isinstance(token, PredicateToken):
#                     num_arguments += 1
#                     stack.append((token, num_arguments))
#                     instructions[-1].append(Instruction(token))
#                     state = State.INVOKE
#                 elif isinstance(token, MarkerToken):
#                     instructions[-1].append(Instruction(token))
#                     num_arguments += 1
#                 else:
#                     raise UnexpectedTokenException(line, element)
#             else:
#                 raise NotRecognizeException(line, element)
#     return list(zip(labels, instructions, strings))


def parse_tree(label: LabelToken,
               instructions: List[Instruction],
               strings: Dict[int, List[str]],
               collapse_type: str = "dfs") -> Ast:
    if collapse_type == "dfs":
        return dfs_parse_tree(label, instructions, strings)
    if collapse_type == "bfs":
        return bfs_parse_tree(label, instructions, strings)
    raise ValueError("Collapse type hasn't recognize")


def dfs_parse_tree(label: LabelToken,
                   instructions: List[Instruction],
                   strings: Dict[int, List[str]]) -> Ast:
    if len(instructions) == 0:
        UnexpectedEofException()
    tail: Iterator[Tuple[int, Instruction]] = enumerate(instructions)
    idx, instruction = next(tail, (None, None))
    idx, instruction, root = dfs_parse_instruction(idx, instruction, tail, strings)
    if instruction is not None:
        raise ExpectedEofException()
    return Ast(label, root)


def dfs_parse_arguments(token: PredicateToken,
                        tail: Iterator[Tuple[int, Instruction]],
                        strings: Dict[int, List[str]]) -> (List[Node], Instruction):
    num_arguments = token.num_arguments
    result = []
    idx, instruction = next(tail, (None, None))
    while instruction is not None:
        if len(result) == num_arguments:
            return result, idx, instruction
        idx, instruction, node = dfs_parse_instruction(idx, instruction, tail, strings)
        result.append(node)
    if len(result) == num_arguments:
        return result, idx, instruction
    raise UnexpectedEofException()


def dfs_parse_instruction(idx: int,
                          instruction: Instruction,
                          tail: Iterator[Tuple[int, Instruction]],
                          strings: Dict[int, List[str]]) -> (int, Instruction, Node):
    token = instruction.token
    if isinstance(token, StringToken):
        if idx not in strings:
            raise StringInstanceNotFoundException()
        node = StringNode(strings[idx])
        idx, instruction = next(tail, (None, None))
    elif isinstance(token, PredicateToken):
        children, idx, instruction = dfs_parse_arguments(token, tail, strings)
        node = Node(token, children)
    elif isinstance(token, MarkerToken):
        node = Node(token)
        idx, instruction = next(tail, (None, None))
    else:
        raise UnexpectedInstructionException(instruction)
    return idx, instruction, node


def bfs_parse_tree(label: LabelToken,
                   instructions: List[Instruction],
                   strings: Dict[int, List[str]]) -> Ast:
    if len(instructions) == 0:
        raise UnexpectedEofException()
    root, parents = bfs_parse_instruction(0, instructions, strings)
    if isinstance(instructions[0].token, PredicateToken):
        for idx in range(1, len(instructions)):
            parent = parents[idx - 1]
            node, appendix = bfs_parse_instruction(idx, instructions, strings)
            parents.extend(appendix)
            parent.children.append(node)
            node.parent = parent
    elif len(instructions) != 1:
        raise ExpectedEofException()
    return Ast(label, root)


def bfs_parse_instruction(idx: int,
                          instructions: List[Instruction],
                          strings: Dict[int, List[str]]) -> (Node, List[Node]):
    instruction = instructions[idx]
    token = instruction.token
    if isinstance(token, StringToken):
        if idx not in strings:
            raise StringInstanceNotFoundException()
        node = StringNode(strings[idx])
        parents = []
    elif isinstance(token, PredicateToken):
        node = Node(token)
        parents = [node] * token.num_arguments
    elif isinstance(token, MarkerToken):
        node = Node(token)
        parents = []
    else:
        raise UnexpectedInstructionException(instruction)
    return node, parents


def parse(code: str) -> List[Ast]:
    forest = []
    stack = []

    def parse_operator(operator):
        operator = operator[0]
        token = tokens.value_of(operator)
        assert isinstance(token, OperatorToken)
        token = token.predicate
        assert len(stack) >= token.num_arguments
        node = Node(token, stack[-token.num_arguments:])
        del stack[-token.num_arguments:]
        stack.append(node)

    def parse_marker(marker):
        marker = marker[0]
        token = tokens.value_of(marker)
        assert isinstance(token, MarkerToken)
        node = Node(token)
        stack.append(node)

    def parse_predicate(predicate):
        predicate = predicate[0]
        token = tokens.value_of(predicate)
        assert isinstance(token, PredicateToken)
        assert len(stack) >= token.num_arguments
        node = Node(token, stack[-token.num_arguments:])
        del stack[-token.num_arguments:]
        stack.append(node)

    def parse_string(string):
        string = string[0]
        assert len(string) > 0
        if string[0] in quotes:
            assert string[-1] == string[0]
            string = string[1:-1]
        node = StringNode(string.split(" "))
        stack.append(node)

    def parse_label(label):
        label = label[0]
        token = tokens.value_of(label)
        assert isinstance(token, LabelToken)
        assert len(stack) == 1
        ast = Ast(token, stack[0])
        forest.append(ast)
        del stack[0]

    parser = grammar.build(parse_operator, parse_marker, parse_predicate, parse_string, parse_label)
    parser.parseString(code)
    return forest
