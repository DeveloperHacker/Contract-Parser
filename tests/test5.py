import unittest

from contracts import Parser, Decompiler
from contracts.Compiler import BfsCompiler
from contracts.Validator import Validator


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = "strong param[0] == \"Some text\" => param[0] != 'null'"
        tree = Parser.parse(raw_code)
        compiler = BfsCompiler()
        tokens = compiler.accept(tree)
        reverted_tree = Decompiler.bfs(tokens)
        Validator().accept(tree)
        assert reverted_tree == tree
