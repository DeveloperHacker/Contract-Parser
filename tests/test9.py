import unittest

from contracts.guides.AstDfsGuide import AstDfsGuide
from contracts.parser.Parser import parse
from contracts.visitors.AstEqualReducer import AstEqualReducer


class TestCase(unittest.TestCase):
    def test(self):
        raw_tree = (
            "weak",
            " equal",
            "  equal",
            "   string \"this the string\"",
            "   string \"another string\"",
            "  false"
        )
        forest = parse("`true != equal('this the string', 'another string')")
        assert len(forest) == 1
        ast = forest[0]
        assert ast.consistent()
        guide = AstDfsGuide(AstEqualReducer())
        guide.accept(ast)
        assert str(ast) == "\n".join(raw_tree)
