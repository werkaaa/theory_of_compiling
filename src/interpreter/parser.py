#!/usr/bin/python
from . import scanner
from .ast import *
import ply.yacc as yacc


class Parser:
    tokens = scanner.Scanner().tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("nonassoc", 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ("right", 'ASSIGN'),
        ("nonassoc", 'GREATER', 'GREATEREQ', 'SMALLER', 'SMALLEREQ', 'EQ', 'NOTEQ'),
        ("left", 'ADD', 'SUB'),
        ("left", 'MUL', 'DIV'),
        ("left", 'DOTADD', 'DOTSUB'),
        ("left", 'DOTMUL', 'DOTDIV'),
        ("right", 'UMINUS'),
        ("left", 'TRANSPOSE'),
    )

    start = 'program'

    GOT_SYNTAX_ERROR = False

    # Builds the parser
    def __init__(self, lexer):
        self._lexer = lexer.lexer
        self.parser = yacc.yacc(module=self)

    def parse(self, text):
        return self.parser.parse(text)

    @staticmethod
    def p_error(p):
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")
        Parser.GOT_SYNTAX_ERROR = True

    @staticmethod
    def p_program(p):
        """program : instructions_opt """
        p[0] = Program(p[1])

    def p_empty(self, p):
        """empty : """
        pass

    @staticmethod
    def p_instructions_opt(p):
        """instructions_opt : instructions
                            | empty """
        p[0] = p[1]

    @staticmethod
    def p_block_of_instructions(p):
        """block : '{' instructions_opt '}' """
        p[0] = Block(p[2])
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_instructions(p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 2:
            p[0] = Instructions(p[1])
            p[0].lineno = p[1].lineno
        else:
            p[0] = Instructions(p[2], p[1])
            p[0].lineno = p[2].lineno

    @staticmethod
    def p_instruction(p):
        """instruction : assignment ';'
                       | if_instruction
                       | while_instruction
                       | for_instruction
                       | break_instruction ';'
                       | continue_instruction ';'
                       | return_instruction ';'
                       | print_instruction ';'
                       | block """
        p[0] = p[1]
        p[0].lineno = p[1].lineno

    # Expressions
    @staticmethod
    def p_unary_minus(p):
        """expression : SUB expression %prec UMINUS"""
        if len(p) == 3:
            p[0] = UnaryMinus(p[2])
        else:
            p[0] = UnaryMinus(p[3])
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_expression(p):
        """expression : number
                      | array
                      | variable
                      | STRING """
        if isinstance(p[1], str):
            p[0] = String(p[1])
            p[0].lineno = p.lineno(1)
        else:
            p[0] = p[1]
            p[0].lineno = p[1].lineno

    @staticmethod
    def p_binary_operations(p):
        """expression : expression ADD expression
                      | expression SUB expression
                      | expression MUL expression
                      | expression DIV expression """
        p[0] = NumberBinaryOperation(p[1], p[2], p[3])
        p[0].lineno = p.lineno(2)

    @staticmethod
    def p_binary_operations_dot(p):
        """expression : expression DOTADD expression
                      | expression DOTSUB expression
                      | expression DOTMUL expression
                      | expression DOTDIV expression """
        p[0] = MatrixBinaryOperation(p[1], p[2], p[3])
        p[0].lineno = p.lineno(2)

    @staticmethod
    def p_expression_par(p):
        """expression : '(' expression ')' """
        p[0] = p[2]
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_transpose(p):
        """expression : expression TRANSPOSE """
        p[0] = Transpose(p[1])
        p[0].lineno = p.lineno(2)

    @staticmethod
    def p_matrix_func_call(p):
        """expression : matrix_func '(' inner_array ')' """
        p[0] = MatrixFunction(p[1], p[3])
        p[0].lineno = p.lineno(2)

    @staticmethod
    def p_matrix_functions(p):
        """matrix_func : EYE
                       | ZEROS
                       | ONES """
        p[0] = p[1]

    @staticmethod
    def p_binary_relations(p):
        """expression : expression SMALLER expression
                      | expression GREATER expression
                      | expression SMALLEREQ expression
                      | expression GREATEREQ expression
                      | expression NOTEQ expression
                      | expression EQ expression"""
        p[0] = BooleanExpression(p[1], p[2], p[3])
        p[0].lineno = p.lineno(2)

    # Numbers
    @staticmethod
    def p_int(p):
        """number : INTNUM """
        p[0] = IntNum(p[1])
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_float(p):
        """number : FLOATNUM """
        p[0] = FloatNum(p[1])
        p[0].lineno = p.lineno(1)

    # Arrays
    @staticmethod
    def p_array(p):
        """array : '[' ']'
                 | '[' inner_array ']' """
        if len(p) == 3:
            p[0] = Array()
        else:
            p[0] = Array(p[2])
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_inner_array(p):
        """inner_array : inner_array ',' expression
                       | expression """
        if len(p) == 2:
            p[0] = InnerList(p[1])
        else:
            p[0] = InnerList(p[3], p[1])
        p[0].lineno = p[1].lineno

    @staticmethod
    def p_range(p):
        """range : expression ':' expression """
        p[0] = Range(p[1], p[3])
        p[0].lineno = p.lineno(2)

    @staticmethod
    def p_indices_part(p):
        """indices_part : range
                        | expression"""
        p[0] = p[1]
        p[0].lineno = p[1].lineno

    @staticmethod
    def p_list_of_indices(p):
        """list_indices : list_indices ',' indices_part
                        | indices_part """
        if len(p) == 2:
            p[0] = ListOfIndices(p[1])
        else:
            p[0] = ListOfIndices(p[3], p[1])
        p[0].lineno = p[1].lineno

    @staticmethod
    def p_list_of_arguments(p):
        """list_arguments : list_arguments ',' expression
                          | expression """
        if len(p) == 2:
            p[0] = ListOfArguments(p[1])
        else:
            p[0] = ListOfArguments(p[3], p[1])
        p[0].lineno = p[1].lineno

    @staticmethod
    def p_variable(p):
        """variable : ID """
        p[0] = Identifier(p[1])
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_array_variable(p):
        """variable : ID '[' list_indices ']'"""
        identifier = Identifier(p[1])
        identifier.lineno = p.lineno(1)
        p[0] = ArrayElement(identifier, p[3])
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_string_variable(p):
        """variable : STRING '[' list_indices ']'"""
        string = String(p[1])
        string.lineno = p.lineno(1)
        p[0] = ArrayElement(string, p[3])
        p[0].lineno = p.lineno(1)

    # Instructions
    @staticmethod
    def p_assignment(p):
        """assignment : variable ASSIGN expression
                      | variable ADDASSIGN expression
                      | variable SUBASSIGN expression
                      | variable MULASSIGN expression
                      | variable DIVASSIGN expression """
        p[0] = Assignment(p[1], p[2], p[3])
        p[0].lineno = p.lineno(2)

    @staticmethod
    def p_if_else_instruction(p):
        """if_instruction : IF '(' expression ')' instruction %prec IFX
                          | IF '(' expression ')' instruction ELSE instruction """
        if len(p) == 6:
            p[0] = If(p[3], p[5])
        else:
            p[0] = If(p[3], p[5], p[7])
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_while_instruction(p):
        """while_instruction : WHILE '(' expression ')' instruction """
        p[0] = While(p[3], p[5])
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_for_instruction(p):
        """for_instruction : FOR ID ASSIGN range instruction """
        identifier = Identifier(p[2])
        identifier.lineno = p.lineno(1)
        p[0] = For(identifier, p[4], p[5])
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_break_instruction(p):
        """break_instruction : BREAK """
        p[0] = Break()
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_continue_instruction(p):
        """continue_instruction : CONTINUE """
        p[0] = Continue()
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_return_instruction(p):
        """return_instruction : RETURN
                              | RETURN list_arguments """
        if len(p) == 3:
            p[0] = Return(p[2])
        else:
            p[0] = Return()
        p[0].lineno = p.lineno(1)

    @staticmethod
    def p_print_instruction(p):
        """print_instruction : PRINT list_arguments """
        p[0] = Print(p[2])
        p[0].lineno = p.lineno(1)
