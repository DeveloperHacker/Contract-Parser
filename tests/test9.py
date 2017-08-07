import itertools
import unittest

from contracts.guides.AstDfsGuide import AstDfsGuide
from contracts.parser import Parser
from contracts.visitors.AstCompiler import AstCompiler


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = ("not_equal(param[0], null)",
                    "may(param[1], null)",
                    "follow(equal(param[1], null), 'default zone')",
                    "not_equal(param[0], null)",
                    "`not_equal(result, null)",
                    "may(param[0], 'negative')",
                    "not_equal(param[0], null)",
                    "not_equal(param[1], null)",
                    "not_equal(param[2], null)",
                    "follow(equal(param[3], 'null'), param[3] == 'ISOChronology in default zone')",
                    "may(param[3], 'null')",
                    "param[0] is 'valid values defined by the chronology'",
                    "param[1] is 'valid values defined by the chronology'",
                    "param[2] is 'valid values defined by the chronology'",
                    "param[0] is 'the year'",
                    "param[1] is 'the month of the year'",
                    "param[2] is 'the day of the month'",
                    "param[3] is 'the chronology'")
        forest = itertools.chain(*(Parser.parse(raw_line) for raw_line in raw_code))
        compiler = AstDfsGuide(AstCompiler())
        parsed = [compiler.accept(tree) for tree in forest]
        forest = [Parser.parse_tree(*args) for args in parsed]
        assert all(tree.consistent() for tree in forest)
