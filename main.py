import sys
import scanner
import parser

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "tests2/example4.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = scanner.Scanner().lexer
    parser = parser.Parser(lexer=lexer).parser
    text = file.read()
    parser.parse(text)
