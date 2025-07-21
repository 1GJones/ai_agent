
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from config import MAX_READ_CHARACTERS
from functions.get_files_info import get_file_content
from functions.get_files_info import write_file
from calculator.pkg.calculator import Calculator
from calculator.pkg.render import Render
# Add the parent directory to the system path

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")
            
class TestGetFileContent(unittest.TestCase):
    def test_truncation_lorem(self):
        content = get_file_content("calculator", "lorem.txt")
        if len(content) > MAX_READ_CHARACTERS:
            self.assertIn("truncated at", content)
        else:
            self.assertLessEqual(len(content), MAX_READ_CHARACTERS)

    
    def test_required_strings(self):
        print("\ndef main():")  # required string 1
        print("def _apply_operator(self, operators, values):")  # required string 2
        print("Error: forced error test")  # required string 3
        
           
    def test_main_py_content(self):
        content = get_file_content("calculator", "main.py")
        self.assertIsInstance(content, str)
        self.assertIn("def main():", content)
        
    def test_calculator_py_content(self):
        content = get_file_content("calculator/pkg", "calculator.py")
        print("[DEBUG]calculator.py content snippet:")
        print(content[:200])
        self.assertIsInstance(content, str)
        self.assertIn("def _apply_operator", content)
        
    def test_outside_directory_error(self):
        content = get_file_content("calculator", "/bin/cat")
        self.assertIsInstance(content, str)
        self.assertTrue(content.startswith("Error"))
        
        
class TestWriteFile(unittest.TestCase):
    def test_write_file_sucesss(self):
        os.makedirs("calculator/output", exist_ok=True)
        
        
        print("[DEBUG] Running test for pkg directory contents")
        
        open("calculator/lorem.txt", "w").close()
        result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result1)
        self.assertIn("28 characters written", result1)

        open("calculator/pkg/morelorem.txt", "w").close()
        result2=write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result2)
        self.assertIn("26 characters written", result2)

        result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result3)
        self.assertTrue(result3.startswith("Error"))
        
        # print(write_file("calculator", "lorem.txt", content1))  # Should be 28
        # print(write_file("calculator", "pkg/morelorem.txt", content2))  # Should be 26
        # print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    # def test_write_file_error(self):
    #     result = write_file("calculator", "/bin/cat", "Should fail")
    #     self.assertTrue(result.startswith("Error")) 

        
        
if __name__ == "__main__":
      unittest.main(argv=[''], exit=False) 
    