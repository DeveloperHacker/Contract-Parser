from contracts import Types

ROOT = "root"

GETATTR = "."
CONTAIN_PROPERTY = "<-"
NOT_CONTAIN_PROPERTY = "<x"
EQUAL = "=="
NOT_EQUAL = "!="
MAY = "may"
LOWER_OR_EQUAL = "<="
LOWER = "<"
GREATER_OR_EQUAL = ">="
GREATER = ">"
IS = "is"
IS_NOT = "is not"
AND = "and"
OR = "or"
FOLLOW = "=>"

RESULT = "result"
TRUE = "true"
FALSE = "false"
THIS = "this"
_THIS = "~this"
PARAM = "param"

STRONG = "strong"
WEAK = "weak"

instances = {
    Types.LABEL: (STRONG, WEAK),
    Types.MARKER: (RESULT, TRUE, FALSE, THIS, _THIS, PARAM),
    Types.OPERATOR: (GETATTR, CONTAIN_PROPERTY, NOT_CONTAIN_PROPERTY,
                     EQUAL, NOT_EQUAL, MAY, LOWER_OR_EQUAL, LOWER,
                     GREATER_OR_EQUAL, GREATER, IS, IS_NOT, AND, OR, FOLLOW),
    Types.ROOT: (ROOT,)
}
