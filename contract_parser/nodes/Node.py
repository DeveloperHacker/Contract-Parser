from typing import Iterable, List

from contract_parser.Instruction import Instruction
from contract_parser.tokens import tokens
from contract_parser.tokens.Token import Token


class Node:
    def __init__(self, token: Token = None, children: Iterable['Node'] = None):
        self.token: Token = token
        self.children: List[Node] = [] if children is None else list(children)

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def str(self, depth: int) -> Iterable[str]:
        result: List[str] = [" " * depth + self.token.name]
        if not self.is_leaf():
            for child in self.children:
                result.extend(child.str(depth + 1))
        return result

    def flatten(self) -> Iterable[Instruction]:
        result: List[Instruction] = [Instruction(self.token)]
        for child in self.children:
            result.extend(child.flatten())
        if not self.is_leaf():
            result.append(Instruction(tokens.END_ARGS))
        return result
