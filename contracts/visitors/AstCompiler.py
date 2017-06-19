from typing import List, Iterable

from contracts.nodes.Ast import Ast
from contracts.nodes.Node import Node
from contracts.nodes.StringNode import StringNode
from contracts.parser.Instruction import Instruction
from contracts.tokens.LabelToken import LabelToken
from contracts.visitors.AstVisitor import AstVisitor


class AstCompiler(AstVisitor):
    def __init__(self):
        super().__init__()
        self._label = None
        self._instructions = None
        self._strings = None

    def _insert(self, instruction: Instruction):
        self._instructions.append(instruction)

    def _insert_before(self, where: Instruction, instruction: Instruction):
        index = self._instructions.index(where)
        self._instructions[index:index] = (instruction,)

    def _insert_after(self, where: Instruction, instruction: Instruction):
        index = self._instructions.index(where)
        self._instructions[index + 1:index + 1] = (instruction,)

    def _insert_all(self, instructions: List[Instruction]):
        self._instructions.extend(instructions)

    def _insert_before_all(self, where: Instruction, instructions: Iterable[Instruction]):
        index = self._instructions.index(where)
        self._instructions[index:index] = instructions

    def _insert_after_all(self, where: Instruction, instructions: Iterable[Instruction]):
        index = self._instructions.index(where)
        self._instructions[index + 1:index + 1] = instructions

    def result(self) -> (LabelToken, List[Instruction]):
        return self._label, self._instructions, self._strings

    def visit(self, ast: Ast):
        self._label = ast.label
        self._instructions = []
        self._strings = {}

    def visit_node(self, node: Node):
        self._insert(Instruction(node.token))

    def visit_string(self, node: StringNode):
        idx = len(self._instructions) - 1
        self._strings[idx] = node.words
