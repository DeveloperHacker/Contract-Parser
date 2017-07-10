from pyparsing import Word, ZeroOrMore, Forward, Optional, nums, Literal, Keyword, Combine, StringEnd, alphas, Suppress, \
    dblQuotedString, sglQuotedString


def build(parse_operator, parse_marker, parse_predicate, parse_string, parse_label):
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
    attribute = atom + ZeroOrMore((GET_OP + Suppress(string)).setParseAction(parse_operator))
    equation = attribute + ZeroOrMore((equations + Suppress(attribute)).setParseAction(parse_operator))
    expression << (equation + ZeroOrMore((FOLLOW_OP + Suppress(equation)).setParseAction(parse_operator)))
    statement = (Optional(label, default=STRONG.match) + Suppress(expression)).setParseAction(parse_label)
    code = ZeroOrMore(statement) + StringEnd()

    return code
