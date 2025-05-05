import unittest
from calculator.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_basic_operations(self):
        self.assertEqual(self.calc.evaluate("2 + 3"), 5)
        self.assertEqual(self.calc.evaluate("10 - 4"), 6)
        self.assertEqual(self.calc.evaluate("3 * 5"), 15)
        self.assertEqual(self.calc.evaluate("20 / 4"), 5)
        self.assertEqual(self.calc.evaluate("2 ^ 3"), 8)
    
    def test_complex_expressions(self):
        self.assertEqual(self.calc.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(self.calc.evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(self.calc.evaluate("2 + 3 * (4 - 1)"), 11)
        self.assertEqual(self.calc.evaluate("10 / (5 - 3)"), 5)
    
    def test_functions(self):
        self.assertEqual(self.calc.evaluate("sqrt(16)"), 4)
        self.assertEqual(self.calc.evaluate("sin(90)"), 1)
        self.assertEqual(self.calc.evaluate("cos(0)"), 1)
        self.assertAlmostEqual(self.calc.evaluate("tan(45)"), 1, places=10)
        self.assertEqual(self.calc.evaluate("log(100)"), 2)
        self.assertEqual(self.calc.evaluate("log(8, 2)"), 3)
    
    def test_nested_expressions(self):
        self.assertEqual(self.calc.evaluate("sqrt(9) + sin(90) * 10"), 13)
        self.assertEqual(self.calc.evaluate("(2 + 3) * sqrt(16)"), 20)
        self.assertEqual(self.calc.evaluate("log(10 ^ 2)"), 2)
    
    def test_error_handling(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate("10 / 0")
        
        with self.assertRaises(ValueError):
            self.calc.evaluate("2 +")
        
        with self.assertRaises(ValueError):
            self.calc.evaluate("sqrt(-1)")
        
        with self.assertRaises(ValueError):
            self.calc.evaluate("log(-10)")
        
        with self.assertRaises(ValueError):
            self.calc.evaluate("(2 + 3")
    
    def test_whitespace_handling(self):
        self.assertEqual(self.calc.evaluate("2+3"), 5)
        self.assertEqual(self.calc.evaluate(" 2 + 3 "), 5)
        self.assertEqual(self.calc.evaluate("2    +   3"), 5)
    
    def test_empty_expression(self):
        self.assertEqual(self.calc.evaluate(""), 0)

if __name__ == '__main__':
    unittest.main()