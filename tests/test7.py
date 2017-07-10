import unittest

from contracts.parser.Parser import parse_new


class TestCase(unittest.TestCase):
    def test(self):
        forest = parse_new("")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("param[0] != null")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("strong param[0] != null")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("strong param[0] != asd")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("strong equal(this.asd, null)")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("strong equal(this.asd, (null))")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("strong this.field.field")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("strong this.field.field == null => result == null")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("strong this.field.field == (null => result == null)")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("follow(equal(param[0], null), 'in default zone')")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("param[0] == null => 'in default zone'")
        assert all(tree.consistent() for tree in forest)
        forest = parse_new("param[0] == null => 'null'\n`result == null => a == true")
        assert all(tree.consistent() for tree in forest)
