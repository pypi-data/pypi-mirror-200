# COPYRIGHT RadioactiveRocket 2023

import sys
import re

def get_path():
    frame = sys._getframe()
    while frame.f_back:
        frame = frame.f_back

        if frame.f_globals.get('__name__') == '__main__':
            return frame.f_globals['__file__']
        
    return None

def transpile(code):
    keywords = ['and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield', 'match', 'case']

    # Turn hello:"world" into hello("world")

    def replace(match):
        if match.group(2).strip().startswith('#') or match.group(1) in keywords or not match.group(2).strip():
            return match.group(0)
        else:
            return f"{match.group(1)}({match.group(2)})"

    code = re.sub(r'([a-zA-Z_]\w*):([^:\n]+)', replace, code)

    # Turn hint(hello, str) into hello: str.

    def replace(match):
        return f"{match.group(1).strip()}:{match.group(2).strip()}"

    code = re.sub(r'\bhint\s*\(([^,]+),\s*([^)]+)\)', replace, code)

    return code

def run(exit=0):
    path = get_path()
    
    with open(path, "r") as file:
        try:
            code = file.read()

        except FileNotFoundError:
            raise FileNotFoundError("File: '"+path+"' could not be found.")

        try:
            match = re.search(r"""(?:[^"\']|^)import\s+colonpython(?:[^"\']|$)""", code)
            code = code[match.end():].strip()

        except AttributeError:
            raise SyntaxError('Could not find import statement. Try putting "import colonpython" on the first line.')

        code = transpile(code)

    exec(code)

    raise SystemExit(exit)

if __name__ != "__main__":
    run()
else:
    print("Please run code as a module. Thank you!")