from BasicCalculatorFasil import Calculator
import unittest


class test_Calculator((unittest.TestCase)):
    """ This is a class to test basicCalculator package 
    """

    def setUp(self) -> None:
        self.calculator = Calculator()

    def test_add(self):
        self.assertTrue(self.calculator.memory == 0.0)
        self.assertTrue(self.calculator.add(2) == 2.0)
        self.assertTrue(self.calculator.add(2) == 4.0)

    def test_subtract(self):
        self.assertTrue(self.calculator.memory == 0.0)
        self.assertTrue(self.calculator.subtract(2) == -2.0)
        self.assertTrue(self.calculator.subtract(2) == -4.0)

    def test_multiply(self):
        self.assertTrue(self.calculator.memory == 0.0)
        self.assertTrue(self.calculator.multiply(2) == 0.0)
        self.assertTrue(self.calculator.add(2) == 2.0)
        self.assertTrue(self.calculator.multiply(3) == 6.0)

    def test_divide(self):
        self.assertTrue(self.calculator.memory == 0.0)
        self.assertTrue(self.calculator.add(5) == 5.0)
        self.assertTrue(self.calculator.divide(2) == 2.5)

    def test_root(self):
        self.assertTrue(self.calculator.memory == 0.0)
        self.assertTrue(self.calculator.add(9) == 9.0)
        self.assertTrue(self.calculator.root(2) == 3.0)

    @unittest.expectedFailure
    def test_fail(self):
        self.assertTrue(self.calculator.memory == 0)
        self.assertTrue(self.calculator.add(2) == 2)
        self.assertTrue(self.calculator.multiply(2) == 0)


if __name__ == '__main__':
    unittest.main()
