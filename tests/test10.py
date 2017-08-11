import unittest

from contracts import Parser


class TestCase(unittest.TestCase):
    def test(self):
        tree = Parser.parse("param[0] == ('null' => result == 'null')")
        assert str(tree) == "root(strong(==(param[0],=>('null',==(result,'null')))))"
        tree = Parser.parse("'1' <= param[1] and param[1] <= '12' or '1' <= param[2] and param[2] <= '31'")
        raw_tree = "root(strong(or(and(<=('1',param[1]),<=(param[1],'12')),and(<=('1',param[2]),<=(param[2],'31')))))"
        assert str(tree) == raw_tree
        assert tree.height() == 6
        tree = Parser.parse("strong this.field1.field2")
        raw_tree = "root(strong(.(.(this,'field1'),'field2')))"
        assert str(tree) == raw_tree
        assert tree.height() == 5
