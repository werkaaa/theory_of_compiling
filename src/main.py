import sys

from interpreter import parser, type_checker, scanner, interpreter

DEBUG = False

if __name__ == '__main__':

    filename = sys.argv[1] if len(sys.argv) > 1 else "../tests5/example0.m"
    try:
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = scanner.Scanner().lexer
    parser = parser.Parser(lexer=lexer).parser
    text = file.read()
    ast = parser.parse(text)
    if ast is not None:
        if DEBUG:
            ast.printTree()
        typeChecker = type_checker.TypeChecker()
        typeChecker.visit(ast)

        interpreter = interpreter.Interpreter()
        interpreter.visit(ast)