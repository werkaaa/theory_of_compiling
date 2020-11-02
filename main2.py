import os
import sys
import scanner

def main_scanner():
  default_test_file_path = ['tests', 'scanner_tests', 'example_full.txt']
  try:
    filename = sys.argv[1] if len(sys.argv) > 1 else os.path.join(*default_test_file_path) 
    file = open(filename, "r")
  except IOError:
    print("Cannot open {0} file".format(filename))
    sys.exit(0)

  text = file.read()
  lexer = scanner.Scanner().lexer

  # Give the lexer some input
  lexer.input(text)

  # Tokenize
  while True:
    tok = lexer.token()
    if not tok:
      break  # No more input
    print(f'({tok.lineno}): {tok.type}({tok.value})')


def main_parser():
  import Mparser
  default_test_file_path = ['tests', 'parser_tests', 'example0.m']
  try:
    filename = sys.argv[1] if len(sys.argv) > 1 else os.path.join(*default_test_file_path) 
    file = open(filename, "r")
  except IOError:
    print("Cannot open {0} file".format(filename))
    sys.exit(0)

  parser = Mparser.parser
  text = file.read()
  parser.parse(text, lexer=scanner.Scanner().lexer)


if __name__ == '__main__':
    main_parser()

