from contracts import Types

ROOT = "root"

GETATTR = "."
MUL = "*"
DIV = "/"
MOD = "%"
ADD = "+"
SUB = "-"
EQUAL = "=="
NOT_EQUAL = "!="
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
    Types.OPERATOR: (GETATTR, MUL, DIV, MOD, ADD, SUB,
                     EQUAL, NOT_EQUAL, LOWER_OR_EQUAL, LOWER,
                     GREATER_OR_EQUAL, GREATER, IS, IS_NOT, AND, OR, FOLLOW),
    Types.ROOT: (ROOT,)
}

priority = {
    MUL: 0, DIV: 0, MOD: 0,
    ADD: 1, SUB: 1,
    GREATER_OR_EQUAL: 2, GREATER: 2, LOWER_OR_EQUAL: 2, LOWER: 2,
    EQUAL: 3, NOT_EQUAL: 3, IS: 3, IS_NOT: 3,
    AND: 4,
    OR: 5,
    FOLLOW: 6
}
