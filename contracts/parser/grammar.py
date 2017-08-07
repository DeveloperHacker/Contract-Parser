from pyparsing import Word, ZeroOrMore, Forward, Optional, Literal, Keyword, StringEnd, alphas, Suppress, \
    quotedString, MatchFirst, And, Combine, nums

from contracts.tokens import Predicates, Labels, Operators, Markers


def build(parse_operator, parse_marker, parse_predicate, parse_string, parse_label):
    expression = Forward()

    string = quotedString().setParseAction(parse_string)
    attribute_name = Word(alphas).setParseAction(parse_string)

    label = MatchFirst(Keyword(name) for name in Labels.names) | Labels.SHORT_WEAK.name

    escape = (Operators.GET.name, Operators.IS.name, Operators.IS_NOT.name)
    operator = MatchFirst(Literal(name) for name in Operators.names if name not in escape)
    # operator |= Keyword(Operators.IS_NOT.name)
    operator |= And(Keyword(word) for word in Operators.IS_NOT.name.split(" "))
    operator |= Keyword(Operators.IS.name)

    escape = (Markers.PARAM.name, Markers.PARAM_0.name,
              Markers.PARAM_1.name, Markers.PARAM_2.name,
              Markers.PARAM_3.name, Markers.PARAM_4.name)
    marker = MatchFirst(Keyword(name) for name in Markers.names if name not in escape)
    marker |= Combine(Keyword(Markers.PARAM.name) + "[" + Word(nums) + "]")
    marker.setParseAction(parse_marker)

    predicate_name = MatchFirst(Keyword(name) for name in Predicates.instances.keys())
    predicate_arguments = (expression + ZeroOrMore("," + expression)) | Optional(expression)
    predicate = (predicate_name + Suppress("(" + predicate_arguments + ")")).setParseAction(parse_predicate)

    # noinspection PyUnresolvedReferences
    atom = ("(" + expression + ")") | predicate | marker | string
    attribute = atom + ZeroOrMore((Operators.GET.name + Suppress(attribute_name)).setParseAction(parse_operator))
    expression << attribute + ZeroOrMore((operator + Suppress(attribute)).setParseAction(parse_operator))
    statement = (Optional(label, Labels.STRONG.name) + Suppress(expression)).setParseAction(parse_label)

    return ZeroOrMore(statement) + StringEnd()
