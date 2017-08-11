import unittest

from contracts import Parser, Decompiler
from contracts.Compiler import DfsCompiler
from contracts.Validator import Validator


class TestCase(unittest.TestCase):
    def test(self):
        raw_code = ("param[0] != 'null'",
                    "param[1] may 'null'",
                    "param[1] == 'null' => 'default zone'",
                    "param[0] != 'null'",
                    "`result != 'null'",
                    "param[0] may 'negative'",
                    "param[0] != 'null'",
                    "param[1] != 'null'",
                    "param[2] != 'null'",
                    "param[3] == 'null' => param[3] == 'ISOChronology in default zone'",
                    "param[3] may 'null'",
                    "param[0] is 'valid values defined by the chronology'",
                    "param[1] is 'valid values defined by the chronology'",
                    "param[2] is 'valid values defined by the chronology'",
                    "param[0] is 'the year'",
                    "param[1] is 'the month of the year'",
                    "param[2] is 'the day of the month'",
                    "param[3] is 'the chronology'")
        tree = Parser.parse("\n".join(raw_code))
        compiler = DfsCompiler()
        tokens = compiler.accept(tree)
        Decompiler.dfs(tokens)
        Validator().accept(tree)
