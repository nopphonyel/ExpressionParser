import unittest
from expression_parser.simple_parser import SimpleParser


class DefiningTestCase(unittest.TestCase):

    def setUp(self):
        self.exps = SimpleParser()

    def test_define(self):
        # Using lambda for define value
        self.exps.define("lambda1", lambda: 5)
        self.assertEqual(self.exps.eval("lambda1"), 5)

        self.exps.define("แลมด้าไทย", lambda: 10)
        self.assertEqual(self.exps.eval("แลมด้าไทย"), 10)

        # Using a simple numbers for define
        self.exps.define("simple_number", 4)
        self.assertEqual(self.exps.eval("simple_number"), 4)

        def func1():
            return 12 - 30

        self.exps.define("func1_value", func1)
        self.assertEqual(self.exps.eval("func1_value"), func1())

    def test_operator_priority(self):
        self.exps.define("v1", 2)
        self.exps.define("v2", 3)
        self.exps.define("v3", 4)
        self.assertEqual(self.exps.eval("v1+v2*v3"), 14)
        self.assertEqual(self.exps.eval("v1-v2*v3"), -10)
        self.assertEqual(self.exps.eval("(v1+v2)*v3"), 20)
        self.assertEqual(self.exps.eval("(v1-v2)*v3"), -4)


if __name__ == '__main__':
    unittest.main()
