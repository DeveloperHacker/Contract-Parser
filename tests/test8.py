import unittest

from contracts import Parser, Decompiler
from contracts.Compiler import DfsCompiler
from contracts.Validator import Validator


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = "strong 'the field' is 'supported' strong 'the field' is not 'supported'"
        raw_tree = "root(strong(is('the field','supported')),strong(is not('the field','supported')))"
        tree = Parser.parse(raw_code)
        compiler = DfsCompiler()
        tokens = compiler.accept(tree)
        tree = Decompiler.dfs(tokens)
        Validator().accept(tree)
        assert str(tree) == raw_tree
