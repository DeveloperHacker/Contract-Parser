from typing import List, Iterable

from contracts.nodes.Node import Node
from contracts.nodes.RootNode import RootNode
from contracts.nodes.StringNode import StringNode
from contracts.nodes.WordNode import WordNode
from contracts.parser.Instruction import Instruction
from contracts.tokens import tokens
from contracts.visitors.AstVisitor import AstVisitor


class AstCollapser(AstVisitor):
    def __init__(self):
        super().__init__()
        self.instructions = None

    def _insert(self, instruction: Instruction):
        self.instructions.append(instruction)

    def _insert_before(self, where: Instruction, instruction: Instruction):
        index: int = self.instructions.index(where)
        self.instructions[index:index] = (instruction,)

    def _insert_after(self, where: Instruction, instruction: Instruction):
        index: int = self.instructions.index(where)
        self.instructions[index + 1:index + 1] = (instruction,)

    def _insert_all(self, instructions: List[Instruction]):
        self.instructions.extend(instructions)

    def _insert_before_all(self, where: Instruction, instructions: Iterable[Instruction]):
        index: int = self.instructions.index(where)
        self.instructions[index:index] = instructions

    def _insert_after_all(self, where: Instruction, instructions: Iterable[Instruction]):
        index: int = self.instructions.index(where)
        self.instructions[index + 1:index + 1] = instructions

    def _visit(self):
        self.instructions = []

    def _visit_other_node(self, node: Node):
        self._insert(Instruction(node.token))

    def _visit_root(self, node: RootNode):
        self._insert(Instruction(node.token))

    def _visit_word(self, node: WordNode):
        self._insert(Instruction(node.token, node.instance))

    def _visit_other_node_end(self, node: Node):
        if not node.is_leaf(): self._insert(Instruction(tokens.END_ARGS))

    def _visit_string_end(self, node: StringNode):
        self._insert(Instruction(tokens.END_STRING))

    def _visit_end(self):
        self._insert(Instruction(tokens.END))
