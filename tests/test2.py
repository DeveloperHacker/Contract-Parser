import unittest

from contracts.guides.AstDfsGuide import AstDfsGuide
from contracts.parser import Parser
from contracts.visitors.AstDecompiler import AstDecompiler


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = ("  strong not_equal(param[0], null)",
                    "  weak not_equal(param[1], null)",
                    "  strong not_equal(result, null)",
                    "  strong equal(\"The bucket is reset\", true)",
                    "  strong equal(\"The bucket must not be shared\", true)",
                    "  strong equal(\"parsing is not supported\", false)",
                    "  strong equal(\"the text to parse is invalid\", false)")
        parsed = Parser.parse("\n".join(raw_code))
        forest = [Parser.parse_tree(*args) for args in parsed]
        assert all(tree.consistent() for tree in forest)
        guide = AstDfsGuide(AstDecompiler())
        assert all(tree.consistent() for tree in forest)
        code = [guide.accept(tree) for tree in forest]
        assert "\n".join(code) == "\n".join(string.strip() for string in raw_code)
