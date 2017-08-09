import unittest

from contracts.guides.AstDfsGuide import AstDfsGuide
from contracts.parser import Parser
from contracts.visitors.AstCompiler import AstCompiler


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = " strong follow(equal(param[0], null), \"in default zone\")"
        raw_tree = ("strong", " follow", "  equal", "   param[0]", "   null", "  \"in default zone\"")
        forest = Parser.parse(raw_code)
        compiler = AstDfsGuide(AstCompiler())
        parsed = [compiler.accept(tree) for tree in forest]
        assert len(parsed) == 1
        tree = Parser.parse_tree(*parsed[-1])
        assert tree.consistent()
        assert str(tree) == "\n".join(raw_tree)
