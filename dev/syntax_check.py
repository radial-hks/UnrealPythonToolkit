"""
Simple syntax validation for the Unreal Python Processor skill.
This script checks if the generated code has valid Python syntax.
"""

import ast
import sys

def check_syntax(filename):
    """Check if a Python file has valid syntax."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()

        # Try to parse the code
        ast.parse(code)
        print(f"✅ {filename}: Syntax is valid")
        return True

    except SyntaxError as e:
        print(f"❌ {filename}: Syntax error at line {e.lineno}, column {e.offset}")
        print(f"   {e.text}")
        print(f"   {' ' * (e.offset - 1)}^")
        return False

    except FileNotFoundError:
        print(f"❌ {filename}: File not found")
        return False

    except Exception as e:
        print(f"❌ {filename}: Error - {str(e)}")
        return False

def main():
    """Check syntax of all generated Python files."""
    files_to_check = [
        'unreal_python_processor.py',
        'demo_processor_usage.py',
        'syntax_check.py'
    ]

    print("=== Syntax Check ===")

    all_valid = True
    for filename in files_to_check:
        if not check_syntax(filename):
            all_valid = False

    print("\n=== Summary ===")
    if all_valid:
        print("✅ All files have valid Python syntax!")
        print("The Unreal Python Processor skill is ready to use.")
    else:
        print("❌ Some files have syntax errors.")
        print("Please fix the errors before using the skill.")

    return all_valid

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)