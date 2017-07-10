import unittest

from contracts.guides.AstBfsGuide import AstBfsGuide
from contracts.parser import Parser
from contracts.visitors.AstCompiler import AstCompiler


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = "strong follow(equal(param[0], \"Some text\"), not_equal(param[0], null))"
        parsed = Parser.parse(raw_code)
        assert len(parsed) == 1
        tree = Parser.parse_tree(*parsed[-1])
        assert tree.consistent()
        guide = AstBfsGuide(AstCompiler())
        label, instructions, strings = guide.accept(tree)
        reverted_tree = Parser.parse_tree(label, instructions, strings, collapse_type="bfs")
        assert reverted_tree == tree
