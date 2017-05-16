from src.parser.tokens.BracketToken import BracketToken
from src.parser.tokens.FunctionToken import FunctionToken, Type
from src.parser.tokens.LabelToken import LabelToken
from src.parser.tokens.MarkerToken import MarkerToken

# -------------------- Functions -------------------- #
EQUAL = FunctionToken("equal", (Type.ARGUMENT, Type.ARGUMENT,))
NOT_EQUAL = FunctionToken("not_equal", (Type.ARGUMENT, Type.ARGUMENT,))
IS = FunctionToken("is", (Type.ARGUMENT, Type.ARGUMENT,))
FOLLOW = FunctionToken("follow", (Type.ARGUMENT, Type.ARGUMENT,))
MAYBE = FunctionToken("maybe", (Type.ARGUMENT, Type.ARGUMENT,))
AND = FunctionToken("and", (Type.ARGUMENT, Type.ARGUMENT,))
OR = FunctionToken("or", (Type.ARGUMENT, Type.ARGUMENT,))
INSIDE = FunctionToken("inside", (Type.ARGUMENT, Type.VARARG))
LOWER = FunctionToken("lower", (Type.ARGUMENT, Type.ARGUMENT,))
GREATER = FunctionToken("greater", (Type.ARGUMENT, Type.ARGUMENT,))
SATISFY = FunctionToken("satisfy", (Type.ARGUMENT, Type.ARGUMENT,))

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
