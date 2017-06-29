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
from contracts.tokens.PredicateToken import PredicateToken
from contracts.tokens.StringToken import StringToken


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

    class UnexpectedEofException(AnalyseException):
        def __init__(self):
            super().__init__("unexpected the end of the contract")

    class ExpectedEofException(AnalyseException):
        def __init__(self):
            super().__init__("expected the end of the contract")

    class StringInstanceNotFoundException(AnalyseException):
        def __init__(self):
            super().__init__("instance of string hasn't found")

    delimiters = ("(", ")", ",", " ", "\n")
    trash_symbols = (" ", ",", "\n")
    quotes = ("\"", "'")

    staticmethod
    def split(source: str) -> List[str]:
        splited = []
        token = []
        start_string = None
        in_str = False
        open_quote = None
        prev = None
        line = 1
        for ch in source:
            if ch in Parser.quotes:
                if in_str and prev != "\\" and ch == open_quote:
                    in_str = False
                    open_quote = None
                elif not in_str:
                    in_str = True
                    open_quote = ch
                    start_string = line
            if not in_str and ch in (Parser.delimiters + Parser.quotes):
                token = "".join(token).strip()
                if len(token) > 0:
                    splited.append((line, token))
                if ch not in (Parser.trash_symbols + Parser.quotes):
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

    staticmethod
    def is_string(token: str):
        return len(token) > 0 and token[0] in Parser.quotes

    staticmethod
    def parse(source: str) -> (List[Tuple[LabelToken, List[Instruction], Dict[int, List[str]]]]):
        class State(Enum):
            LABEL = 0
            ARGUMENT = 1
            INVOKE = 2

        strings: List[Dict[int, List[str]]] = []
        instructions: List[List[Instruction]] = []
        labels: List[LabelToken] = []
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
                    instructions.append([])
                    strings.append({})
                    labels.append(token)
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
                    instructions[-1].append(Instruction(tokens.STRING))
                    strings[-1][len(instructions[-1]) - 1] = element[1:].split(" ")
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
                        instructions[-1].append(Instruction(token))
                        state = State.INVOKE
                    elif isinstance(token, MarkerToken):
                        instructions[-1].append(Instruction(token))
                        num_arguments += 1
                    else:
                        raise Parser.UnexpectedTokenException(line, element)
                else:
                    raise Parser.NotRecognizeException(line, element)
        return list(zip(labels, instructions, strings))

    staticmethod
    def parse_tree(label: LabelToken,
                   instructions: List[Instruction],
                   strings: Dict[int, List[str]],
                   collapse_type: str = "dfs") -> Ast:
        if collapse_type == "dfs":
            return Parser.dfs_parse_tree(label, instructions, strings)
        if collapse_type == "bfs":
            return Parser.bfs_parse_tree(label, instructions, strings)
        raise ValueError("Collapse type hasn't recognize")

    staticmethod
    def dfs_parse_tree(label: LabelToken,
                       instructions: List[Instruction],
                       strings: Dict[int, List[str]]) -> Ast:
        if len(instructions) == 0:
            Parser.UnexpectedEofException()
        tail: Iterator[Tuple[int, Instruction]] = enumerate(instructions)
        idx, instruction = next(tail, (None, None))
        if not isinstance(instruction.token, PredicateToken):
            raise Parser.UnexpectedInstructionException(instruction)
        node = Node(instruction.token)
        ast = Ast(label, node)
        node.children, idx, instruction = Parser.parse_arguments(instruction.token, tail, strings)
        if instruction is not None:
            raise Parser.ExpectedEofException()
        return ast

    staticmethod
    def parse_arguments(token: PredicateToken,
                        tail: Iterator[Tuple[int, Instruction]],
                        strings: Dict[int, List[str]]) -> (List[Node], Instruction):
        result = []
        idx, instruction = next(tail, (None, None))
        while instruction is not None:
            if len(result) == token.num_arguments:
                return result, idx, instruction
            if isinstance(instruction.token, StringToken):
                if idx not in strings:
                    raise Parser.StringInstanceNotFoundException()
                node = StringNode(strings[idx])
                idx, instruction = next(tail, (None, None))
                result.append(node)
            elif isinstance(instruction.token, PredicateToken):
                node = Node(instruction.token)
                node.children, idx, instruction = Parser.parse_arguments(instruction.token, tail, strings)
                result.append(node)
            elif isinstance(instruction.token, MarkerToken):
                node = Node(instruction.token)
                idx, instruction = next(tail, (None, None))
                result.append(node)
            else:
                raise Parser.UnexpectedInstructionException(instruction)
        if len(result) == token.num_arguments:
            return result, idx, instruction
        raise Parser.UnexpectedEofException()

    staticmethod
    def bfs_parse_tree(label: LabelToken,
                       instructions: List[Instruction],
                       strings: Dict[int, List[str]]) -> Ast:
        if len(instructions) == 0:
            Parser.UnexpectedEofException()
        instruction = instructions[0]
        token = instruction.token
        if not isinstance(token, PredicateToken):
            raise Parser.UnexpectedInstructionException(instruction)
        node = Node(token)
        ast = Ast(label, node)
        parents: List[Node] = [node] * token.num_arguments
        current_idx = 1
        while current_idx < len(instructions):
            parent = parents[current_idx - 1]
            current = instructions[current_idx]
            if isinstance(current.token, StringToken):
                if current_idx not in strings:
                    raise Parser.StringInstanceNotFoundException()
                node = StringNode(strings[current_idx])
                parent.children.append(node)
            elif isinstance(current.token, PredicateToken):
                node = Node(current.token)
                parent.children.append(node)
                parents.extend([node] * current.token.num_arguments)
            elif isinstance(current.token, MarkerToken):
                node = Node(current.token)
                parent.children.append(node)
            else:
                raise Parser.UnexpectedInstructionException(instructions[current_idx])
            current_idx += 1
        return ast

    @staticmethod
    def parse_new(code: str) -> List[Ast]:
        forest = []
        stack = []

        def parse_operation(_operation):
            print("operation:", _operation)

        def parse_marker(_marker):
            print("marker:", _marker)

        def parse_predicate(_predicate):
            print("predicate:", _predicate)

        def parse_string(_string):
            print("string:", _string)

        def parse_label(_label):
            print("label:", _label)

        parser = grammar.build(parse_operation, parse_marker, parse_predicate, parse_string, parse_label)
        parser.parseString(code)
        return forest


def main():
    # Parser.parse_new("")
    # Parser.parse_new("param[0] != null")
    # Parser.parse_new("strong param[0] != null")
    # Parser.parse_new("strong param[0] != asd")
    # Parser.parse_new("strong equal(this.asd, null)")
    # Parser.parse_new("strong equal(this.asd, (null))")
    # Parser.parse_new("strong this.field.field")
    # Parser.parse_new("strong this.field.field == null => result == null")
    # Parser.parse_new("strong this.field.field == (null => result == null)")
    # Parser.parse_new("follow(equal(param[0], null), 'in default zone')")
    # Parser.parse_new("param[0] == null => 'in default zone'")
    Parser.parse_new("param[0] == null => 'null'\n`result == null => a == true")


if __name__ == '__main__':
    main()
