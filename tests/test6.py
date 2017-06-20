from contracts.parser.Parser import Parser


def run():
    raw_code = " strong follow(equal(@param[0], @null), \"in default zone\")"
    raw_tree = ("strong",
                " follow",
                "  equal",
                "   @param[0]",
                "   @null",
                "  @string \"in default zone\"")
    parsed = Parser.parse(raw_code)
    assert len(parsed) == 1
    tree = Parser.parse_tree(*parsed[-1])
    assert str(tree) == "\n".join(raw_tree)
