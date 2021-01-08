import sys

import interpreter
import parser
import scanner
import tree_printer
import type_checker

if __name__ == '__main__':

  try:
    filename = sys.argv[1] if len(sys.argv) > 1 else "tests5/example0.m"
    file = open(filename, "r")
  except IOError:
    print("Cannot open {0} file".format(filename))
    sys.exit(0)

  lexer = scanner.Scanner().lexer
  parser = parser.Parser(lexer=lexer).parser
  text = file.read()
  ast = parser.parse(text)
  if ast is not None:
    #ast.printTree()
    typeChecker = type_checker.TypeChecker()
    typeChecker.visit(ast)

    interpreter = interpreter.Interpreter()
    interpreter.visit(ast)


