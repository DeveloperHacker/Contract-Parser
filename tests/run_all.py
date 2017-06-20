import unittest

from tests import test1, test2, test3, test4, test5, test6


class TestCase(unittest.TestCase):
    def test1(self):
        test1.run()

    def test2(self):
        test2.run()

    def test3(self):
        test3.run()

    def test4(self):
        test4.run()

    def test5(self):
        test5.run()

    def test6(self):
        test6.run()

if __name__ == '__main__':
    unittest.main()
