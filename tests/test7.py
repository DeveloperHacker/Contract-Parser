import unittest

from contracts import Parser


class TestCase(unittest.TestCase):
    def test(self):
        Parser.parse("")
        Parser.parse("param[0] != 'null'")
        Parser.parse("strong param[0] != 'null'")
        Parser.parse("strong param[0] != 'asd'")
        Parser.parse("strong this.asd == 'null'")
        Parser.parse("strong this.asd == ('null')")
        Parser.parse("strong this.field.field")
        Parser.parse("strong this.field.field == 'null' => result == 'null'")
        Parser.parse("strong this.field.field == ('null' => result == 'null')")
        Parser.parse("param[0] == 'null' => 'in default zone'")
        Parser.parse("param[0] == 'null' => 'null'\n`result == 'null' => 'a' == true")
        Parser.parse("\n".join(["'1' <= param[1]", "param[1] <= '12'", "'1' <= param[2]", "param[2] <= '31'"]))
        Parser.parse("param[0] may 'negative'")
        Parser.parse("'1' <= param[1] and param[1] <= '12'")
        Parser.parse("'1' <= param[1] and param[1] <= '12' or '1' <= param[2] and param[2] <= '31'")
        Parser.parse("strong get(get(this, 'field'), 'field')")
        Parser.parse("this.years <x 'contains' this.months <x 'contains'")
