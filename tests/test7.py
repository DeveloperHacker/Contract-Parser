import unittest

from contracts.parser.Parser import parse


class TestCase(unittest.TestCase):
    def test(self):
        forest = parse("")
        assert all(tree.consistent() for tree in forest)
        forest = parse("param[0] != null")
        assert all(tree.consistent() for tree in forest)
        forest = parse("strong param[0] != null")
        assert all(tree.consistent() for tree in forest)
        forest = parse("strong param[0] != asd")
        assert all(tree.consistent() for tree in forest)
        forest = parse("strong equal(this.asd, null)")
        assert all(tree.consistent() for tree in forest)
        forest = parse("strong equal(this.asd, (null))")
        assert all(tree.consistent() for tree in forest)
        forest = parse("strong this.field.field")
        assert all(tree.consistent() for tree in forest)
        forest = parse("strong this.field.field == null => result == null")
        assert all(tree.consistent() for tree in forest)
        forest = parse("strong this.field.field == (null => result == null)")
        assert all(tree.consistent() for tree in forest)
        forest = parse("follow(equal(param[0], null), 'in default zone')")
        assert all(tree.consistent() for tree in forest)
        forest = parse("param[0] == null => 'in default zone'")
        assert all(tree.consistent() for tree in forest)
        forest = parse("param[0] == null => 'null'\n`result == null => a == true")
        assert all(tree.consistent() for tree in forest)
