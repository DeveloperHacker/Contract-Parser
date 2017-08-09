import unittest

from contracts.parser.Parser import parse


class TestCase(unittest.TestCase):
    def test(self):
        forest = parse("param[0] == 'null' => result == 'null'")
        assert len(forest) == 1
        print(forest[0])
