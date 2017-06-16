import unittest


class TestCase(unittest.TestCase):
    def test1(self):
        from tests import test1
        test1.run()

    def test2(self):
        from tests import test2
        test2.run()

    def test3(self):
        from tests import test3
        test3.run()

    def test4(self):
        from tests import test4
        test4.run()


if __name__ == '__main__':
    unittest.main()
