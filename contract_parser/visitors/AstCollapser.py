from typing import List, Iterable

from contract_parser.Instruction import Instruction
from contract_parser.nodes.Node import Node
from contract_parser.nodes.RootNode import RootNode
from contract_parser.nodes.StringNode import StringNode
from contract_parser.nodes.WordNode import WordNode
from contract_parser.tokens import tokens
from contract_parser.visitors.AstVisitor import TreeVisitor


class TreeCollapser(TreeVisitor):
    def __init__(self):
        super().__init__()
        self.instructions: List[Instruction] = None

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
