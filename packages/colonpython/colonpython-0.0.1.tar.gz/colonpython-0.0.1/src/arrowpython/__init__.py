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
    code = re.sub(r'(?<!\')(?:=>)(?!\')', ':', code)

    code = re.sub(r'([a-zA-Z_]\w*):([^:\n]+)', r'\1(\2)', code)

    return code

def run(exit=0):
    path = get_path()

    with open(path, "r") as file:
        try:
            code = file.read()

        except FileNotFoundError:
            raise FileNotFoundError("File: '"+path+"' could not be found.")

        try:
            match = re.search(r"""(?:[^"\']|^)import\s+arrowpython(?:[^"\']|$)""", code)
            code = code[match.end():].strip()

        except AttributeError:
            raise SyntaxError('Could not find import statement. Try putting "import arrowpython" on the first line.')

        code = transpile(code)

    exec(code)

    raise SystemExit(exit)

if __name__ != "main":
    run()
else:
    print("Please run code as a module. Thank you!")