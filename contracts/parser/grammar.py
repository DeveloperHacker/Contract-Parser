from typing import List

from pyparsing import Word, ZeroOrMore, Forward, Optional, nums, Literal, Keyword, Combine, StringEnd, alphas, Suppress, \
    dblQuotedString, sglQuotedString

from contracts.nodes.Ast import Ast


def build(parse_operation, parse_marker, parse_predicate, parse_string, parse_label):
    left_bracket = Literal("(")
    right_bracket = Literal(")")
    left_square_bracket = Literal("[")
    right_square_bracket = Literal("]")
    comma = Literal(",")
    number = Word(nums)
    string = dblQuotedString() | sglQuotedString() | Word(alphas)

    # predicates
    EQUAL = Keyword("equal")
    NOT_EQUAL = Keyword("not_equal")
    MAYBE = Keyword("maybe")
    LOWER = Keyword("lower")
    GREATER = Keyword("greater")
    FOLLOW = Keyword("follow")
    GET = Keyword("get")

    # markers
    NULL = Keyword("null")
    TRUE = Keyword("true")
    FALSE = Keyword("false")
    PARAM = Combine(Keyword("param") + left_square_bracket + number + right_square_bracket)
    RESULT = Keyword("result")
    ZERO = Keyword("0")
    THIS = Keyword("this")
    PRE_THIS = Keyword("pre_this")
    POST_THIS = Keyword("post_this")

    # labels
    STRONG = Keyword("strong")
    WEAK = Keyword("weak")
    SHORT_WEAK = Literal("`")

    # operators
    EQUAL_OP = Literal("==")
    NOT_EQUAL_OP = Literal("!=")
    MAYBE_OP = Literal("?=")
    LOWER_OP = Literal("<")
    GREATER_OP = Literal(">")
    LOWER_OR_EQUAL_OP = Literal("<=")
    GREATER_OR_EQUAL_OP = Literal(">=")
    FOLLOW_OP = Literal("=>")
    GET_OP = Literal(".")

    expression = Forward()

    label = STRONG | WEAK | SHORT_WEAK
    equations = EQUAL_OP | NOT_EQUAL_OP | MAYBE_OP | LOWER_OP | GREATER_OP | LOWER_OR_EQUAL_OP | GREATER_OR_EQUAL_OP
    marker = NULL | TRUE | FALSE | PARAM | RESULT | ZERO | THIS | PRE_THIS | POST_THIS
    predicates = EQUAL | NOT_EQUAL | MAYBE | LOWER | GREATER | FOLLOW | GET

    predicate_arguments = (expression + ZeroOrMore(comma + expression)) | Optional(expression)
    predicate = predicates + Suppress(left_bracket + predicate_arguments + right_bracket)

    marker.setParseAction(parse_marker)
    predicate.setParseAction(parse_predicate)
    string.setParseAction(parse_string)

    atom = (left_bracket + expression + right_bracket) | predicate | marker | string
    attribute = atom + ZeroOrMore((GET_OP + Suppress(string)).setParseAction(parse_operation))
    equation = attribute + ZeroOrMore((equations + Suppress(attribute)).setParseAction(parse_operation))
    expression << (equation + ZeroOrMore((FOLLOW_OP + Suppress(equation)).setParseAction(parse_operation)))
    statement = (Optional(label, default=STRONG) + Suppress(expression)).setParseAction(parse_label)
    code = ZeroOrMore(statement) + StringEnd()

    return code


def parse(code: str) -> List[Ast]:
    forest = []
    stack = []

    def parse_operation(_operation):
        print("operation:", _operation)

    def parse_marker(_marker):
        print("marker:", _marker)

    def parse_predicate(_predicate):
        print("predicate:", _predicate)

    def parse_string(_string):
        print("string:", _string)

    def parse_label(_label):
        print("label:", _label)

    parser = build(parse_operation, parse_marker, parse_predicate, parse_string, parse_label)
    parser.parseString(code)
    return forest


def main():
    # parse("")
    # parse("param[0] != null")
    # parse("strong param[0] != null")
    # parse("strong param[0] != asd")
    # parse("strong equal(this.asd, null)")
    # parse("strong equal(this.asd, (null))")
    # parse("strong this.field.field")
    # parse("strong this.field.field == null => result == null")
    # parse("strong this.field.field == (null => result == null)")
    # parse("follow(equal(param[0], null), 'in default zone')")
    # parse("param[0] == null => 'in default zone'")
    parse("param[0] == null => 'null'"
          "`result == null => a == true")


if __name__ == '__main__':
    main()
