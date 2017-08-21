import unittest

from contracts import Parser, Decompiler
from contracts.Compiler import DfsCompiler
from contracts.Validator import Validator


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = ("result == 'false'",
                    "this is not 'supported'")
        tree = Parser.parse("\n".join(raw_code))
        compiler = DfsCompiler()
        tokens = compiler.accept(tree)
        Decompiler.dfs(tokens)
        Validator().accept(tree)
