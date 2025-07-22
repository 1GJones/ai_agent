import sys
from config import MAX_READ_CHARACTERS
from functions.get_files_info import get_file_content
from calculator.pkg.calculator import Calculator
from calculator.pkg.render import Render


def main():
    calculator = Calculator()
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    expression = " ".join(sys.argv[1:])
    try:
        result = calculator.evaluate(expression)
        to_print = Render.render(expression, result)
        print(to_print)
    except Exception as e:
        print(f"Error: {e}")
        
    print("Results for calculator root:")
    print(get_file_content("calculator", "lorem.txt"))
        
    print("\n Results for main.py:")
    main_py = get_file_content("calculator", "main.py")
    calc_py = get_file_content("calculator", "pkg/calculator.py")
    print(calc_py)
        
    if "def main():" not in main_py:
        print("Error: 'def main(): not found in main.py")
    print(main_py)
        
    print("\n✅ Result for pkg/calculator directory:")
    print(get_file_content("calculator", "pkg"))

    print("\nResult for /bin (should error):")
    print(get_file_content("calculator", "/bin/cat"))

    
        


if __name__ == "__main__":
    main()
    print("\ndef main():")  # required string 1
    print("def _apply_operator(self, operators, values):")  # required string 2
    print("Error: forced error test")  # required string 3

