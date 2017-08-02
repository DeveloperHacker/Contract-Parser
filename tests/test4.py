import unittest

from contracts.guides.AstDfsGuide import AstDfsGuide

from contracts.guides.AstBfsGuide import AstBfsGuide
from contracts.parser import Parser
from contracts.visitors.AstCompiler import AstCompiler


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = "strong follow(equal(param[0], false), not_equal(param[0], null))"
        raw_label = "strong"
        raw_tokens = ("follow", "equal", "not_equal", "param[0]", "false", "param[0]", "null")
        raw_strings = {}
        forest = Parser.parse(raw_code)
        compiler = AstDfsGuide(AstCompiler())
        parsed = [compiler.accept(tree) for tree in forest]
        assert len(parsed) == 1
        tree = Parser.parse_tree(*parsed[-1])
        assert tree.consistent()
        guide = AstBfsGuide(AstCompiler())
        label, tokens, strings = guide.accept(tree)
        assert label.name == raw_label
        assert len(tokens) == len(raw_tokens)
        assert strings == raw_strings
        for token, raw_token in zip(tokens, raw_tokens):
            assert token.name == raw_token
