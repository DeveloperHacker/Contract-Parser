from typing import List

from contracts.nodes.Forest import Forest
from contracts.parser.Instruction import Instruction
from contracts.parser.Parser import Parser
from contracts.visitors.AstBfsVisitor import AstBfsVisitor
from contracts.visitors.AstCompiler import AstCompiler


def run():
    code = ("                strong not_equal(@param[0], @null)",
            "                weak not_equal(@param[1], @null)",
            "                strong not_equal(@result, @null)",
            "                strong equal(\"The bucket is reset\", @true)",
            "                strong equal(\"The bucket must not be shared\", @true)",
            "                strong equal(\"parsing is not supported\", @false)",
            "                strong follow(equal(@param[0], @false), not_equal(@param[0], @null))")

    raw_instructions = ("strong",
                        "follow",
                        "equal",
                        "not_equal",
                        "@param[0]",
                        "@false",
                        "@param[0]",
                        "@null")

    instructions: List[Instruction] = Parser.parse("\n".join(code))
    tree: Forest = Parser.tree(instructions)
    visitor = AstBfsVisitor()
    compiler = AstCompiler()
    visitor.accept(tree.trees[-1], compiler)
    instructions = compiler.instructions
    assert len(instructions) == len(raw_instructions)
    assert all(str(instruct) == raw_instruct for instruct, raw_instruct in zip(instructions, raw_instructions))
