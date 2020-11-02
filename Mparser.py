#!/usr/bin/python

import scanner
import ply.yacc as yacc

from ast import *

tokens = scanner.Scanner.tokens
#tokens = [t for t in tokens if t not in ['BREAK', 'CONTINUE', 'ELSE', 'FOR', 'IF', 'BREAK', 'FOR', 'WHILE', 'PRINT', 'RETURN']]
#tokens += ['ARRAY']

precedence = (
    ("nonassoc", 'GREATER', 'GREATEREQ', 'SMALLER', 'SMALLEREQ', 'EQ', 'NOTEQ'),
    ("nonassoc", 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ("right", 'ASSIGN'),
    ("left", 'ADD', 'SUB'),
    ("left", 'MUL', 'DIV'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", 'DOTMUL', 'DOTDIV'),
    ("left", 'TRANSPOSE'),
    ("right", 'UMINUS'),
)

start = 'PROGRAM'

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

def p_program(p):
    """PROGRAM : INSTRUCTIONS_OPT"""
    p[0] = p[1]

def p_empty(p):
    """EMPTY :"""
    pass

def p_instructions_opt(p):
    """INSTRUCTIONS_OPT : INSTRUCTIONS
                        | EMPTY """
    p[0] = p[1]


def p_instructions(p):
    """INSTRUCTIONS : INSTRUCTIONS INSTRUCTION
                    | INSTRUCTION """
    if len(p) == 2:
        p[0] = Instructions(None, p[1])
    else:
        p[0] = Instructions(p[1], p[2])

def p_instruction(p):
    """INSTRUCTION : EXPRESSION ';'
                   | ASSIGNMENT ';' """
    p[0] = p[1]

# Expressions
def p_expression(p):
    """EXPRESSION : NUMBER
                  | MATRIX
                  | VARIABLE """
    p[0] = p[1]

def p_unary_minus(p):
    """EXPRESSION : SUB NUMBER   %prec UMINUS
                  | SUB VARIABLE %prec UMINUS
                  | SUB MATRIX   %prec UMINUS
                  | SUB '(' EXPRESSION ')' %prec UMINUS """
    if len(p) == 3:
        p[0] = UnaryMinus(p[2])
    else:
        p[0] = UnaryMinus(p[3])

def p_binary_operations(p):
    """EXPRESSION : EXPRESSION ADD EXPRESSION
                  | EXPRESSION SUB EXPRESSION
                  | EXPRESSION MUL EXPRESSION
                  | EXPRESSION DIV EXPRESSION """
    p[0] = NumberBinaryOperation(p[1], p[2], p[3])

def p_binary_operations_dot(p):
    """EXPRESSION : EXPRESSION DOTADD EXPRESSION
                  | EXPRESSION DOTSUB EXPRESSION
                  | EXPRESSION DOTMUL EXPRESSION
                  | EXPRESSION DOTDIV EXPRESSION """
    p[0] = MatrixBinaryOperation(p[1], p[2], p[3])

def p_expression_par(p):
    """EXPRESSION : '(' EXPRESSION ')' """
    p[0] = p[2]

def p_transpose(p):
    """EXPRESSION : EXPRESSION TRANSPOSE """
    p[0] = Transpose(p[1])

def p_matrix_functions(p):
    """EXPRESSION : EYE '(' EXPRESSION ')'
                  | ZEROS '(' EXPRESSION ')'
                  | ONES '(' EXPRESSION ')'
                  | ZEROS '(' EXPRESSION ',' EXPRESSION ')'
                  | ONES '(' EXPRESSION ',' EXPRESSION ')' """

    if len(p) == 7:
        p[0] = MatrixFunction(p[1], p[3], p[5])
    else:
        p[0] = MatrixFunction(p[1], p[3], None)

# Numbers
def p_int(p):
    """NUMBER : INTNUM """
    p[0] = IntNum(p[1])

def p_float(p):
    """NUMBER : FLOATNUM """
    p[0] = FloatNum(p[1])

# Matrix
def p_matrix(p):
    """MATRIX : ROWS """ 
    p[0] = p[1]

def p_rows(p):
    """ROWS : '[' ARRAYS ']' """
    p[0] = p[2]

def p_arrays(p):
    """ARRAYS : ARRAY
              | ARRAYS ',' ARRAY """
    if len(p) == 2:
        p[0] = Arrays(None, p[1])
    else:
        p[0] = Arrays(p[1], p[3])

def p_array(p):
    """ARRAY : ARRAY ',' EXPRESSION
             | EXPRESSION """
    if len(p) == 2:
        p[0] = Array(None, p[1])
    else:
        p[0] = Array(p[1], p[3])

def p_variable(p):
    """VARIABLE : ID """
    p[0] = Identifier(p[1])

#def p_variable_arr


def p_binary_relations(p):
    """BOOLEAN_EXPRESSION : EXPRESSION SMALLER EXPRESSION
                          | EXPRESSION GREATER EXPRESSION
                          | EXPRESSION SMALLEREQ EXPRESSION
                          | EXPRESSION GREATEREQ EXPRESSION
                          | EXPRESSION NOTEQ EXPRESSION
                          | EXPRESSION EQ EXPRESSION
                          | EXPRESSION """
    if len(p) == 2:
        p[0] = p[1]  # Expression as a relation value
    else:
        p[0] = BooleanExpression(p[1], p[2], p[3])

def p_assignment(p):
    """ASSIGNMENT : VARIABLE ASSIGN EXPRESSION
                  | VARIABLE ADDASSIGN EXPRESSION
                  | VARIABLE SUBASSIGN EXPRESSION
                  | VARIABLE MULASSIGN EXPRESSION
                  | VARIABLE DIVASSIGN EXPRESSION """
    p[0] = Assignment(p[1], p[2], p[3])


def p_assignment_string(p):
    """ASSIGNMENT : VARIABLE ASSIGN STRING """
    p[0] = Assignment(p[1], p[2], String(p[3]))    




parser = yacc.yacc()
