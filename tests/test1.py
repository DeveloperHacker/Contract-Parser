import unittest

from contracts.guides.AstDfsGuide import AstDfsGuide
from contracts.parser import Parser
from contracts.visitors.AstCompiler import AstCompiler


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = ("  strong not_equal(param[0], null)",
                    "  weak not_equal(param[1], null)",
                    "  strong not_equal(result, null)",
                    "  strong equal(\"The bucket is reset\", true)",
                    "  strong equal(\"The bucket must not be shared\", true)",
                    "  strong equal(\"parsing is not supported\", false)",
                    "  strong equal('the text to parse is invalid', false)")
        raw_parsed = (("strong", ("not_equal", "param[0]", "null"), {}),
                      ("weak", ("not_equal", "param[1]", "null"), {}),
                      ("strong", ("not_equal", "result", "null"), {}),
                      ("strong", ("equal", "string", "true"), {1: ["The", "bucket", "is", "reset"]}),
                      ("strong", ("equal", "string", "true"), {1: ["The", "bucket", "must", "not", "be", "shared"]}),
                      ("strong", ("equal", "string", "false"), {1: ["parsing", "is", "not", "supported"]}),
                      ("strong", ("equal", "string", "false"), {1: ["the", "text", "to", "parse", "is", "invalid"]}))
        raw_forest = (("strong", " not_equal", "  param[0]", "  null"),
                      ("weak", " not_equal", "  param[1]", "  null"),
                      ("strong", " not_equal", "  result", "  null"),
                      ("strong", " equal", "  string \"The bucket is reset\"", "  true"),
                      ("strong", " equal", "  string \"The bucket must not be shared\"", "  true"),
                      ("strong", " equal", "  string \"parsing is not supported\"", "  false"),
                      ("strong", " equal", "  string \"the text to parse is invalid\"", "  false"))
        parsed = Parser.parse("\n".join(raw_code))
        assert len(parsed) == len(raw_parsed)
        for (label, instructions, strings), (raw_label, raw_instructions, raw_strings) in zip(parsed, raw_parsed):
            assert label.name == raw_label
            assert strings == raw_strings
            for instruction, raw_instruction in zip(instructions, raw_instructions):
                assert str(instruction) == raw_instruction
        forest = [Parser.parse_tree(*args) for args in parsed]
        assert all(tree.consistent() for tree in forest)
        assert len(forest) == len(raw_forest)
        for tree, raw_tree in zip(forest, raw_forest):
            assert str(tree) == "\n".join(raw_tree)
        guide = AstDfsGuide(AstCompiler())
        parsed = [guide.accept(tree) for tree in forest]
        assert len(parsed) == len(raw_parsed)
        for (label, instructions, strings), (raw_label, raw_instructions, raw_strings) in zip(parsed, raw_parsed):
            assert label.name == raw_label
            assert strings == raw_strings
            for instruction, raw_instruction in zip(instructions, raw_instructions):
                assert str(instruction) == raw_instruction
