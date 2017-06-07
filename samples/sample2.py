from contracts.nodes.StringNode import StringNode
from contracts.nodes.WordNode import WordNode
from contracts.parser.Parser import Parser
from contracts.visitors.AstVisitor import AstVisitor


def apply_filters(string: str) -> str:
    # noinspection SqlNoDataSourceInspection
    return "begin {} end".format(string)


class StringFiltrator(AstVisitor):
    def _visit_string(self, node: StringNode):
        string = " ".join(word.instance for word in node.children)
        string = apply_filters(string)
        node.children = [WordNode(word) for word in string.split(" ")]


if __name__ == '__main__':
    code = "                not_equal(@param[0], @null)\n" + \
           "                not_equal(@param[1], @null)\n" + \
           "                not_equal(@result, @null)\n" + \
           "                strong equal(\"The bucket is reset\", @true)\n" + \
           "                strong equal(\"The bucket must not be shared\", @true)\n" + \
           "                equal(\"parsing is not supported\", @false)\n" + \
           "                equal(\"the text to parse is invalid\", @false)\n"

    instructions = Parser.parse(code)
    tree = Parser.tree(instructions)
    print(tree)
    print()
    filtrator = StringFiltrator()
    filtrator.accept(tree)
    print(tree)
