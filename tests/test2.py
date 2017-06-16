from contracts.parser.Parser import Parser
from contracts.visitors.AstDecompiler import AstDecompiler
from contracts.visitors.AstDfsVisitor import AstDfsVisitor


def run():
    code = ("                strong not_equal(@param[0], @null)",
            "                weak not_equal(@param[1], @null)",
            "                strong not_equal(@result, @null)",
            "                strong equal(\"The bucket is reset\", @true)",
            "                strong equal(\"The bucket must not be shared\", @true)",
            "                strong equal(\"parsing is not supported\", @false)",
            "                strong equal(\"the text to parse is invalid\", @false)")

    instructions = Parser.parse("\n".join(code))
    tree = Parser.tree(instructions)
    visitor = AstDfsVisitor()
    decompiler = AstDecompiler()
    visitor.accept(tree, decompiler)
    assert str(decompiler) == "\n".join(string.strip() for string in code)
