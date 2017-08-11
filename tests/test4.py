import unittest

from contracts import Parser, Decompiler
from contracts.Compiler import DfsCompiler, BfsCompiler
from contracts.Validator import Validator


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = "param[0] == false => param[0] != 'null'"
        raw_tokens = ("root", "strong", "=>", "==", "!=", "param[0]", "false", "param[0]", "'null'")
        tree = Parser.parse(raw_code)
        compiler = DfsCompiler()
        tokens = compiler.accept(tree)
        tree = Decompiler.dfs(tokens)
        Validator().accept(tree)
        compiler = BfsCompiler()
        tokens = compiler.accept(tree)
        assert len(tokens) == len(raw_tokens)
        assert all(token.name == raw_token for token, raw_token in zip(tokens, raw_tokens))
