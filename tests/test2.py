import unittest

from contracts import Parser, Decompiler
from contracts.Compiler import DfsCompiler
from contracts.Shower import Shower
from contracts.Validator import Validator


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = ("  strong param[0] != 'null'",
                    "  weak param[1] != 'null'",
                    "  strong result != 'null'",
                    "  strong 'The bucket is reset' == true",
                    "  strong 'The bucket must not be shared' == true",
                    "  strong 'parsing is not supported' == false",
                    "  strong 'the text to parse is invalid' == false")
        tree = Parser.parse("\n".join(raw_code))
        compiler = DfsCompiler()
        tokens = compiler.accept(tree)
        tree = Decompiler.dfs(tokens)
        Validator().accept(tree)
        code = Shower().accept(tree)
        assert "\n".join(code) == "\n".join(string.strip() for string in raw_code)
