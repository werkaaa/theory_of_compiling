import os
import sys
import scanner

# For portability
default_test_file_path = ['tests', 'example1.txt']

def main():
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

if __name__ == '__main__':
    main()

