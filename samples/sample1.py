from contracts.Parser import Parser
from typing import List

from contracts.nodes.Ast import Tree
from contracts.parser.Instruction import Instruction
from contracts.visitors.AstCollapser import AstCollapser

if __name__ == '__main__':
    code = "                not_equal(@param[0], @null)\n" + \
           "                not_equal(@param[1], @null)\n" + \
           "                not_equal(@result, @null)\n" + \
           "                strong is(\"The bucket is reset\", @true)\n" + \
           "                strong is(\"The bucket must not be shared\", @true)\n" + \
           "                is(\"parsing is not supported\", @false)\n" + \
           "                is(\"the text to parse is invalid\", @false)\n"

    instructions: List[Instruction] = Parser.parse(code)
    print("\n".join(str(instruction) for instruction in instructions))
    print()
    tree: Tree = Parser.tree(instructions)
    print(tree)
    print()
    instructions: List[Instruction] = tree.flatten()
    print("\n".join(str(instruction) for instruction in instructions))
    print()
    collapser: AstCollapser = AstCollapser()
    collapser.accept(tree)
    print("\n".join(str(instruction) for instruction in collapser.instructions))
