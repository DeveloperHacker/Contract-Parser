from typing import List

from contracts.nodes.Forest import Forest
from contracts.parser.Instruction import Instruction
from contracts.parser.Parser import Parser
from contracts.visitors.AstCompiler import AstCompiler
from contracts.visitors.AstDfsVisitor import AstDfsVisitor


def run():
    code = ("                strong not_equal(@param[0], @null)",
            "                weak not_equal(@param[1], @null)",
            "                strong not_equal(@result, @null)",
            "                strong equal(\"The bucket is reset\", @true)",
            "                strong equal(\"The bucket must not be shared\", @true)",
            "                strong equal(\"parsing is not supported\", @false)",
            "                strong equal(\"the text to parse is invalid\", @false)")

    raw_instructions = ("strong",
                        "not_equal",
                        "@param[0]",
                        "@null",
                        "weak",
                        "not_equal",
                        "@param[1]",
                        "@null",
                        "strong",
                        "not_equal",
                        "@result",
                        "@null",
                        "strong",
                        "equal",
                        "@string",
                        "@word ~ The",
                        "@word ~ bucket",
                        "@word ~ is",
                        "@word ~ reset",
                        "@true",
                        "strong",
                        "equal",
                        "@string",
                        "@word ~ The",
                        "@word ~ bucket",
                        "@word ~ must",
                        "@word ~ not",
                        "@word ~ be",
                        "@word ~ shared",
                        "@true",
                        "strong",
                        "equal",
                        "@string",
                        "@word ~ parsing",
                        "@word ~ is",
                        "@word ~ not",
                        "@word ~ supported",
                        "@false",
                        "strong",
                        "equal",
                        "@string",
                        "@word ~ the",
                        "@word ~ text",
                        "@word ~ to",
                        "@word ~ parse",
                        "@word ~ is",
                        "@word ~ invalid",
                        "@false")

    raw_tree = ("strong",
                " not_equal",
                "  @param[0]",
                "  @null",
                "weak",
                " not_equal",
                "  @param[1]",
                "  @null",
                "strong",
                " not_equal",
                "  @result",
                "  @null",
                "strong",
                " equal",
                "  @string {",
                "   @word ~ The",
                "   @word ~ bucket",
                "   @word ~ is",
                "   @word ~ reset",
                "  }",
                "  @true",
                "strong",
                " equal",
                "  @string {",
                "   @word ~ The",
                "   @word ~ bucket",
                "   @word ~ must",
                "   @word ~ not",
                "   @word ~ be",
                "   @word ~ shared",
                "  }",
                "  @true",
                "strong",
                " equal",
                "  @string {",
                "   @word ~ parsing",
                "   @word ~ is",
                "   @word ~ not",
                "   @word ~ supported",
                "  }",
                "  @false",
                "strong",
                " equal",
                "  @string {",
                "   @word ~ the",
                "   @word ~ text",
                "   @word ~ to",
                "   @word ~ parse",
                "   @word ~ is",
                "   @word ~ invalid",
                "  }",
                "  @false")

    instructions: List[Instruction] = Parser.parse("\n".join(code))
    assert len(instructions) == len(raw_instructions)
    assert all(str(instruct) == raw_instruct for instruct, raw_instruct in zip(instructions, raw_instructions))
    tree: Forest = Parser.tree(instructions)
    assert str(tree) == "\n".join(raw_tree)
    visitor = AstDfsVisitor()
    compiler = AstCompiler()
    visitor.accept(tree, compiler)
    instructions = compiler.instructions
    assert len(instructions) == len(raw_instructions)
    assert all(str(instruct) == raw_instruct for instruct, raw_instruct in zip(instructions, raw_instructions))
