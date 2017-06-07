from typing import List

from contracts.nodes.Ast import Ast
from contracts.parser.Instruction import Instruction
from contracts.parser.Parser import Parser
from contracts.visitors.AstCompiler import AstCompiler

if __name__ == '__main__':
    code = "                not_equal(@param[0], @null)\n" + \
           "                not_equal(@param[1], @null)\n" + \
           "                not_equal(@result, @null)\n" + \
           "                strong equal(\"The bucket is reset\", @true)\n" + \
           "                strong equal(\"The bucket must not be shared\", @true)\n" + \
           "                equal(\"parsing is not supported\", @false)\n" + \
           "                equal(\"the text to parse is invalid\", @false)\n"

    instructions: List[Instruction] = Parser.parse(code)
    print("\n".join(str(instruction) for instruction in instructions))
    print()
    tree: Ast = Parser.tree(instructions)
    print(tree)
    print()
    collapser: AstCompiler = AstCompiler()
    collapser.accept(tree)
    print("\n".join(str(instruction) for instruction in collapser.instructions))
