import unittest

from src.calculator_package_GUSAEZG.calculator import Calculator


class TestCalculator(unittest.TestCase):

    def test_add(self):
        """Test whether Calculator method add adds argument to memory"""
        calculator = Calculator()
        addend = 10
        self.assertEqual(calculator.add(addend), 10, "Incorrect result")

    def test_subtract(self):
        """Test whether Calculator method subtract subtracts argument to memory"""

        calculator = Calculator()
        subtrahend = 10
        self.assertEqual(calculator.subtract(subtrahend), -10, "Incorrect result")

    def test_multiply(self):
        """Test whether Calculator method multiply multiplies argument by memory"""
        calculator = Calculator()
        calculator.add(10)
        multiplicand = 10
        self.assertEqual(calculator.multiply(multiplicand), 100, "Incorrect result")

    def test_division(self):
        """Test whether Calculator method divide divides memory by argument"""
        calculator = Calculator()
        calculator.add(10)
        divisor = 10
        self.assertEqual(calculator.divide(divisor), 1, "Incorrect result")

    def test_calculate_nth_root(self):
        """Test whether Calculator method calculate_nth_root calculates root using argument as degree"""
        calculator = Calculator()
        calculator.add(100)
        degree = 2
        self.assertEqual(calculator.calculate_nth_root(degree), 10, "Incorrect result")

    def test_reset_memory(self):
        """Test whether Calculator method reset_memory resets memory to 0"""
        calculator = Calculator()
        calculator.add(100)
        calculator.reset_memory()
        self.assertEqual(calculator.memory, 0)

    def test_not_a_number(self):
        """Test whether Calculator private method __assert_number raises AssertionError if argument is not a number"""
        calculator = Calculator()
        with self.assertRaises(AssertionError):
            calculator.add("Not a number")

    def test_root_degree_is_zero(self):
        """Test whether Calculator method calculate_nth_root raises AssertionError if argument is 0"""
        calculator = Calculator()
        with self.assertRaises(AssertionError):
            calculator.calculate_nth_root(0)


if __name__ == '__main__':
    unittest.main()
