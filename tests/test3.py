from contracts.nodes.StringNode import StringNode
from contracts.nodes.WordNode import WordNode
from contracts.parser.Parser import Parser
from contracts.visitors.AstDfsVisitor import AstDfsVisitor
from contracts.visitors.AstVisitor import AstVisitor


def apply_filters(string: str) -> str:
    # noinspection SqlNoDataSourceInspection
    return "begin {} end".format(string)


class StringFiltrator(AstVisitor):
    def visit_string(self, node: StringNode):
        string = " ".join(word.instance for word in node.children)
        string = apply_filters(string)
        node.children = [WordNode(word) for word in string.split(" ")]


def run():
    code = ("                strong not_equal(@param[0], @null)",
            "                weak not_equal(@param[1], @null)",
            "                strong not_equal(@result, @null)",
            "                strong equal(\"The bucket is reset\", @true)",
            "                strong equal(\"The bucket must not be shared\", @true)",
            "                strong equal(\"parsing is not supported\", @false)",
            "                strong equal(\"the text to parse is invalid\", @false)")
    filtered_raw_tree = ("strong",
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
                         "   @word ~ begin",
                         "   @word ~ The",
                         "   @word ~ bucket",
                         "   @word ~ is",
                         "   @word ~ reset",
                         "   @word ~ end",
                         "  }",
                         "  @true",
                         "strong",
                         " equal",
                         "  @string {",
                         "   @word ~ begin",
                         "   @word ~ The",
                         "   @word ~ bucket",
                         "   @word ~ must",
                         "   @word ~ not",
                         "   @word ~ be",
                         "   @word ~ shared",
                         "   @word ~ end",
                         "  }",
                         "  @true",
                         "strong",
                         " equal",
                         "  @string {",
                         "   @word ~ begin",
                         "   @word ~ parsing",
                         "   @word ~ is",
                         "   @word ~ not",
                         "   @word ~ supported",
                         "   @word ~ end",
                         "  }",
                         "  @false",
                         "strong",
                         " equal",
                         "  @string {",
                         "   @word ~ begin",
                         "   @word ~ the",
                         "   @word ~ text",
                         "   @word ~ to",
                         "   @word ~ parse",
                         "   @word ~ is",
                         "   @word ~ invalid",
                         "   @word ~ end",
                         "  }",
                         "  @false")
    instructions = Parser.parse("\n".join(code))
    tree = Parser.tree(instructions)
    visitor = AstDfsVisitor()
    filtrator = StringFiltrator()
    visitor.accept(tree, filtrator)
    assert str(tree) == "\n".join(filtered_raw_tree)
