import unittest

from contracts.guides.AstDfsGuide import AstDfsGuide
from contracts.parser import Parser
from contracts.visitors.AstCompiler import AstCompiler


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = ("strong 'the field' is 'supported'",
                    "strong 'the field' is not 'supported'")
        raw_tree = (("strong", " is_", "  \"the field\"", "  \"supported\""),
                    ("strong", " is_not", "  \"the field\"", "  \"supported\""))
        forest = Parser.parse("\n".join(raw_code))
        compiler = AstDfsGuide(AstCompiler())
        parsed = [compiler.accept(tree) for tree in forest]
        forest = [Parser.parse_tree(*args) for args in parsed]
        for tree, raw_tree in zip(forest, raw_tree):
            assert tree.consistent()
            assert str(tree) == "\n".join(raw_tree)
