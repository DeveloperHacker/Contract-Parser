from contracts.parser.Parser import Parser
from contracts.visitors.AstDecompiler import AstDecompiler

if __name__ == '__main__':
    code = "                strong not_equal(@param[0], @null)\n" + \
           "                weak not_equal(@param[1], @null)\n" + \
           "                strong not_equal(@result, @null)\n" + \
           "                strong equal(\"The bucket is reset\", @true)\n" + \
           "                strong equal(\"The bucket must not be shared\", @true)\n" + \
           "                strong equal(\"parsing is not supported\", @false)\n" + \
           "                strong equal(\"the text to parse is invalid\", @false)\n"

    instructions = Parser.parse(code)
    print("\n".join(str(inst) for inst in instructions))
    tree = Parser.tree(instructions)
    decompiler = AstDecompiler()
    decompiler.accept(tree)
    print(decompiler)
