from contracts.tokens.BracketToken import BracketToken
from contracts.tokens.PredicateToken import PredicateToken, Type
from contracts.tokens.LabelToken import LabelToken

from contracts.tokens.MarkerToken import MarkerToken

# -------------------- Functions -------------------- #
EQUAL = PredicateToken("equal", (Type.ARGUMENT, Type.ARGUMENT,))
NOT_EQUAL = PredicateToken("not_equal", (Type.ARGUMENT, Type.ARGUMENT,))
IS = PredicateToken("is", (Type.ARGUMENT, Type.ARGUMENT,))
FOLLOW = PredicateToken("follow", (Type.ARGUMENT, Type.ARGUMENT,))
MAYBE = PredicateToken("maybe", (Type.ARGUMENT, Type.ARGUMENT,))
AND = PredicateToken("and", (Type.ARGUMENT, Type.ARGUMENT,))
OR = PredicateToken("or", (Type.ARGUMENT, Type.ARGUMENT,))
INSIDE = PredicateToken("inside", (Type.ARGUMENT, Type.VARARG))
LOWER = PredicateToken("lower", (Type.ARGUMENT, Type.ARGUMENT,))
GREATER = PredicateToken("greater", (Type.ARGUMENT, Type.ARGUMENT,))
SATISFY = PredicateToken("satisfy", (Type.ARGUMENT, Type.ARGUMENT,))

# -------------------- Variables -------------------- #
NUM_PARAMS = 5
PARAM_0 = MarkerToken("@param[0]")
PARAM_1 = MarkerToken("@param[1]")
PARAM_2 = MarkerToken("@param[2]")
PARAM_3 = MarkerToken("@param[3]")
PARAM_4 = MarkerToken("@param[4]")
PARAM = MarkerToken("@param")
ZERO = MarkerToken("@zero")
WORD = MarkerToken("@word")
STRING = MarkerToken("@string")
END_STRING = MarkerToken("@end_string")
RESULT = MarkerToken("@result")
NULL = MarkerToken("@null")
TRUE = MarkerToken("@true")
FALSE = MarkerToken("@false")
END_ARGS = MarkerToken("@end_args")
END = MarkerToken("@end")

# -------------------- Labels -------------------- #
UNDEFINED = LabelToken("undefined")
STRONG = LabelToken("strong")
WEAK = LabelToken("weak")

# -------------------- Brackets -------------------- #
LB = BracketToken("(")
RB = BracketToken(")")
