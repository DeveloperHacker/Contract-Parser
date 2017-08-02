import unittest

from contracts.guides.AstDfsGuide import AstDfsGuide

from contracts.guides.AstBfsGuide import AstBfsGuide
from contracts.parser import Parser
from contracts.visitors.AstCompiler import AstCompiler


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = "strong follow(equal(param[0], \"Some text\"), not_equal(param[0], null))"
        forest = Parser.parse(raw_code)
        compiler = AstDfsGuide(AstCompiler())
        parsed = [compiler.accept(tree) for tree in forest]
        assert len(parsed) == 1
        tree = Parser.parse_tree(*parsed[-1])
        assert tree.consistent()
        guide = AstBfsGuide(AstCompiler())
        label, tokens, strings = guide.accept(tree)
        reverted_tree = Parser.parse_tree(label, tokens, strings, bypass="bfs")
        assert reverted_tree == tree
