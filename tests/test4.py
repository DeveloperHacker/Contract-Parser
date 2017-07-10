import unittest

from contracts.guides.AstBfsGuide import AstBfsGuide
from contracts.parser import Parser
from contracts.visitors.AstCompiler import AstCompiler


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = "strong follow(equal(param[0], false), not_equal(param[0], null))"
        raw_label = "strong"
        raw_instructions = ("follow", "equal", "not_equal", "param[0]", "false", "param[0]", "null")
        raw_strings = {}
        parsed = Parser.parse(raw_code)
        assert len(parsed) == 1
        tree = Parser.parse_tree(*parsed[-1])
        assert tree.consistent()
        guide = AstBfsGuide(AstCompiler())
        label, instructions, strings = guide.accept(tree)
        assert label.name == raw_label
        assert len(instructions) == len(raw_instructions)
        assert strings == raw_strings
        for instructions, raw_instructions in zip(instructions, raw_instructions):
            assert str(instructions) == raw_instructions
