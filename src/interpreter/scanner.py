"""
Script with Scanner class.

For each lexem scanner returns its token, line number and the lexem itself.
"""
import ply.lex as lex


# noinspection PySingleQuotedDocstring,PyPep8Naming
class Scanner:
    # Literals declaration
    literals = ['(', ')', '[', ']', '{', '}', ':', ',', ';']

    # Reserved words declaration
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES',
        'print': 'PRINT'}

    # Tokens declaration
    tokens = [
                 'ADD',
                 'SUB',
                 'MUL',
                 'DIV',
                 'DOTADD',
                 'DOTSUB',
                 'DOTMUL',
                 'DOTDIV',
                 'ASSIGN',
                 'ADDASSIGN',
                 'SUBASSIGN',
                 'MULASSIGN',
                 'DIVASSIGN',
                 'SMALLER',
                 'GREATER',
                 'SMALLEREQ',
                 'GREATEREQ',
                 'NOTEQ',
                 'EQ',
                 'TRANSPOSE',
                 'ID',
                 'INTNUM',
                 'FLOATNUM',
                 'STRING'] + list(reserved.values())

    # Simple tokens values
    t_ADD = r'\+'
    t_SUB = r'-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_DOTADD = r'\.\+'
    t_DOTSUB = r'\.-'
    t_DOTMUL = r'\.\*'
    t_DOTDIV = r'\./'
    t_ASSIGN = r'='
    t_SMALLER = r'<'
    t_GREATER = r'>'
    t_SMALLEREQ = r'<='
    t_GREATEREQ = r'>='
    t_NOTEQ = r'!='
    t_EQ = r'=='
    t_TRANSPOSE = r'\''
    t_ADDASSIGN = r'\+='
    t_SUBASSIGN = r'-='
    t_MULASSIGN = r'\*='
    t_DIVASSIGN = r'/='

    t_ignore = '  \t'

    # Builds the lexer
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Handles comments
    def t_COMMENT(self, t):
        r'\#.*'
        pass

    # Token functions definitions
    @staticmethod
    def t_FLOATNUM(t):
        r'((\d+\.\d*)|(\.\d+))((E|e)[+-]?\d+)?'
        t.value = float(t.value)
        return t

    @staticmethod
    def t_INTNUM(t):
        r'\d+'
        t.value = int(t.value)
        return t

    @staticmethod
    def t_STRING(t):
        r'"[^"\n]*"'
        t.value = t.value[1:-1]
        return t

    @staticmethod
    def t_ID(t):
        r'[a-zA-Z_]\w*'
        t.type = Scanner.reserved.get(t.value, 'ID')
        return t

    # Counts new lines
    @staticmethod
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Informs about incorrect input
    @staticmethod
    def t_error(t):
        if t.value[0] == '"':
            print(f'Error({t.lineno}): Illegal character \'"\''
                  ' - missing closing double-quote character in the line')
        else:
            print(f"Error({t.lineno}): Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
