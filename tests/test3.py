import unittest

from contracts.guides.AstDfsGuide import AstDfsGuide
from contracts.nodes.StringNode import StringNode
from contracts.parser import Parser
from contracts.visitors.AstVisitor import AstVisitor


def apply_filters(string: str) -> str:
    # noinspection SqlNoDataSourceInspection
    return "begin {} end".format(string)


class StringFiltrator(AstVisitor):
    def visit_string(self, node: StringNode):
        string = " ".join(node.words)
        string = apply_filters(string)
        node.words = string.split(" ")


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = ("  strong not_equal(param[0], null)",
                    "  weak not_equal(param[1], null)",
                    "  strong not_equal(result, null)",
                    "  strong equal(\"The bucket is reset\", true)",
                    "  strong equal(\"The bucket must not be shared\", true)",
                    "  strong equal(\"parsing is not supported\", false)",
                    "  strong equal(\"the text to parse is invalid\", false)")
        raw_forest = (("strong", " not_equal", "  param[0]", "  null"),
                      ("weak", " not_equal", "  param[1]", "  null"),
                      ("strong", " not_equal", "  result", "  null"),
                      ("strong", " equal", "  string \"begin The bucket is reset end\"", "  true"),
                      ("strong", " equal", "  string \"begin The bucket must not be shared end\"", "  true"),
                      ("strong", " equal", "  string \"begin parsing is not supported end\"", "  false"),
                      ("strong", " equal", "  string \"begin the text to parse is invalid end\"", "  false"))
        parsed = Parser.parse("\n".join(raw_code))
        forest = [Parser.parse_tree(*args) for args in parsed]
        assert all(tree.consistent() for tree in forest)
        guide = AstDfsGuide(StringFiltrator())
        for tree in forest:
            guide.accept(tree)
        assert all(tree.consistent() for tree in forest)
        assert len(forest) == len(raw_forest)
        for tree, raw_tree in zip(forest, raw_forest):
            assert str(tree) == "\n".join(raw_tree)
