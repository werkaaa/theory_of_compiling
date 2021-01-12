import sys

import interpreter as inter

DEBUG = False

if __name__ == '__main__':

    filename = sys.argv[1] if len(sys.argv) > 1 else "../tests5/example0.m"
    try:
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = inter.Scanner()
    parser = inter.Parser(lexer=lexer)
    text = file.read()
    ast = parser.parse(text)

    if ast is None or inter.Parser.GOT_SYNTAX_ERROR or inter.Scanner.GOT_LEXICAL_ERROR:
        sys.exit(0)

    if DEBUG:
        ast.printTree()

    typeChecker = inter.TypeChecker()
    typeChecker.visit(ast)
    if typeChecker.GOT_ERROR:
        sys.exit(0)

    interpreter = inter.Interpreter()
    interpreter.visit(ast)
