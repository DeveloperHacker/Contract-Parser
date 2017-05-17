from typing import List

from contract_parser.Instruction import Instruction
from contract_parser.Parser import Parser
from contract_parser.nodes.Ast import Tree
from contract_parser.visitors.AstCollapser import TreeCollapser

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
    collapser: TreeCollapser = TreeCollapser()
    collapser.accept(tree)
    print("\n".join(str(instruction) for instruction in collapser.instructions))
