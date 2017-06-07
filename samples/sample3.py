from contracts.parser.Parser import Parser
from contracts.visitors.AstDecompiler import AstDecompiler

if __name__ == '__main__':
    code = "                not_equal(@param[0], @null)\n" + \
           "                not_equal(@param[1], @null)\n" + \
           "                not_equal(@result, @null)\n" + \
           "                strong: equal(\"The bucket is reset\", @true)\n" + \
           "                strong: equal(\"The bucket must not be shared\", @true)\n" + \
           "                equal(\"parsing is not supported\", @false)\n" + \
           "                equal(\"the text to parse is invalid\", @false)\n"

    instructions = Parser.parse(code)
    print("\n".join(str(inst) for inst in instructions))
    tree = Parser.tree(instructions)
    decompiler = AstDecompiler()
    decompiler.accept(tree)
    print(decompiler)
