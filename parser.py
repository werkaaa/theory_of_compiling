#!/usr/bin/python

import scanner
import ply.yacc as yacc

from ast import *

class Parser:
  tokens = scanner.Scanner().tokens

  precedence = (
    ("nonassoc", ':'),
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
    ("nonassoc", 'GREATER', 'GREATEREQ', 'SMALLER', 'SMALLEREQ', 'EQ', 'NOTEQ'),
    ("nonassoc", 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ("right", 'ASSIGN'),
    ("right", 'ID', 'STRING', '['),
    ("left", 'ADD', 'SUB'),
    ("left", 'MUL', 'DIV'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", 'DOTMUL', 'DOTDIV'),
    ("right", 'UMINUS'),
    ("left", 'TRANSPOSE'),
  )

  start = 'PROGRAM'

  # Builds the parser
  def __init__(self, lexer):
    self._lexer = lexer
    self.parser = yacc.yacc(module=self)

  def p_error(self, p):
    if p:
      print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
      print("Unexpected end of input")

  def p_program(self, p):
    """PROGRAM : INSTRUCTIONS_OPT"""
    p[0] = p[1]

  def p_empty(self, p):
    """EMPTY :"""
    pass

  def p_instructions_opt(self, p):
    """INSTRUCTIONS_OPT : INSTRUCTIONS
                        | EMPTY """
    p[0] = p[1]

  def p_block_of_instructions(self, p):
    """BLOCK : '{' INSTRUCTIONS_OPT '}'"""
    p[0] = Block(p[2])
    p[0].lineno = p.lineno(0)

  def p_instructions(self, p):
    """INSTRUCTIONS : INSTRUCTIONS INSTRUCTION
                    | INSTRUCTION """
    if len(p) == 2:
      p[0] = Instructions(None, p[1])
    else:
      p[0] = Instructions(p[1], p[2])
    p[0].lineno = p.lineno(0)

  def p_instruction(self, p):
    """INSTRUCTION : EXPRESSION ';'
                   | ASSIGNMENT ';'
                   | IF_INSTRUCTION
                   | WHILE_INSTRUCTION
                   | FOR_INSTRUCTION
                   | BREAK_INSTRUCTION ';'
                   | CONTINUE_INSTRUCTION ';'
                   | RETURN_INSTRUCTION ';'
                   | PRINT_INSTRUCTION ';'
                   | BLOCK """
    p[0] = p[1]

  # Expressions
  def p_expression(self, p):
    """EXPRESSION : NUMBER
                  | ARRAY
                  | VARIABLE
                  | STRING"""
    p[0] = p[1]

  def p_unary_minus(self, p):
    """EXPRESSION : SUB NUMBER   %prec UMINUS
                  | SUB VARIABLE %prec UMINUS
                  | SUB ARRAY   %prec UMINUS
                  | SUB '(' EXPRESSION ')' %prec UMINUS """
    if len(p) == 3:
      p[0] = UnaryMinus(p[2])
    else:
      p[0] = UnaryMinus(p[3])
    p[0].lineno = p.lineno(0)

  def p_binary_operations(self, p):
    """EXPRESSION : EXPRESSION ADD EXPRESSION
                  | EXPRESSION SUB EXPRESSION
                  | EXPRESSION MUL EXPRESSION
                  | EXPRESSION DIV EXPRESSION """
    p[0] = NumberBinaryOperation(p[1], p[2], p[3])
    p[0].lineno = p.lineno(0)

  def p_binary_operations_dot(self, p):
    """EXPRESSION : EXPRESSION DOTADD EXPRESSION
                  | EXPRESSION DOTSUB EXPRESSION
                  | EXPRESSION DOTMUL EXPRESSION
                  | EXPRESSION DOTDIV EXPRESSION """
    p[0] = MatrixBinaryOperation(p[1], p[2], p[3])
    p[0].lineno = p.lineno(0)

  def p_expression_par(self, p):
    """EXPRESSION : '(' EXPRESSION ')' """
    p[0] = p[2]
    p[0].lineno = p.lineno(0)

  def p_transpose(self, p):
    """EXPRESSION : EXPRESSION TRANSPOSE """
    p[0] = Transpose(p[1])
    p[0].lineno = p.lineno(0)

  def p_matrix_functions(self, p):
    """EXPRESSION : EYE '(' EXPRESSION ')'
                  | ZEROS '(' EXPRESSION ')'
                  | ONES '(' EXPRESSION ')'
                  | ZEROS '(' EXPRESSION ',' EXPRESSION ')'
                  | ONES '(' EXPRESSION ',' EXPRESSION ')' """

    if len(p) == 7:
      p[0] = MatrixFunction(p[1], p[3], p[5])
    else:
      p[0] = MatrixFunction(p[1], p[3], None)
    p[0].lineno = p.lineno(0)

  # Numbers
  def p_int(self, p):
    """NUMBER : INTNUM """
    p[0] = IntNum(p[1])
    p[0].lineno = p.lineno(0)

  def p_float(self, p):
    """NUMBER : FLOATNUM """
    p[0] = FloatNum(p[1])
    p[0].lineno = p.lineno(0)

  # Arrays
  def p_array(self, p):
    """ARRAY : '[' INNER_ARRAY ']'"""
    p[0] = p[2]

  def p_inner_array(self, p):
    """INNER_ARRAY : EXPRESSION ',' INNER_ARRAY
                   | EXPRESSION"""
    if len(p)==2:
      p[0] = InnerList(p[1])
    else:
      p[0] = InnerList(p[1], p[3])

    p[0].lineno = p.lineno(0)

  def p_range_list_indices(self, p):
    """LIST_INDICES : RANGE ',' LIST_INDICES
                    | RANGE"""
    if len(p)==2:
      p[0] = InnerList(p[1])
    else:
      p[0] = InnerList(p[1], p[3])

    p[0].lineno = p.lineno(0)

  def p_expression_list_indices(self, p):
    """LIST_INDICES : EXPRESSION ',' LIST_INDICES
                    | EXPRESSION"""
    if len(p)==2:
      p[0] = InnerList(p[1])
    else:
      p[0] = InnerList(p[1], p[3])

    p[0].lineno = p.lineno(0)

  def p_variable(self, p):
    """VARIABLE : ID """
    p[0] = Identifier(p[1])
    p[0].lineno = p.lineno(0)

  def p_array_variable(self, p):
    """VARIABLE : ID '[' LIST_INDICES ']'"""
    p[0] = ArrayElement(Identifier(p[1]), p[3])
    p[0].lineno = p.lineno(0)

  def p_string_variable(self, p):
    """VARIABLE : STRING '[' LIST_INDICES ']'"""
    p[0] = ArrayElement(p[1], p[3])
    p[0].lineno = p.lineno(0)

  def p_binary_relations(self, p):
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
    p[0].lineno = p.lineno(0)

  def p_assignment(self, p):
    """ASSIGNMENT : VARIABLE ASSIGN EXPRESSION
                  | VARIABLE ADDASSIGN EXPRESSION
                  | VARIABLE SUBASSIGN EXPRESSION
                  | VARIABLE MULASSIGN EXPRESSION
                  | VARIABLE DIVASSIGN EXPRESSION """
    p[0] = Assignment(p[1], p[2], p[3])
    p[0].lineno = p.lineno(0)


  def p_if_else_instruction(self, p):
    """IF_INSTRUCTION : IF '(' BOOLEAN_EXPRESSION ')' INSTRUCTION %prec IFX
                      | IF '(' BOOLEAN_EXPRESSION ')' INSTRUCTION ELSE INSTRUCTION"""
    if len(p) == 6:
      p[0] = If(p[3], p[5], None)
    else:
      p[0] = If(p[3], p[5], p[7])
    p[0].lineno = p.lineno(0)

  def p_while_instruction(self, p):
    """WHILE_INSTRUCTION : WHILE '(' BOOLEAN_EXPRESSION ')' INSTRUCTION"""
    p[0] = While(p[3], p[5])
    p[0].lineno = p.lineno(0)

  def p_range(self, p):
    """RANGE : EXPRESSION ':' EXPRESSION"""
    p[0] = Range(p[1], p[3])
    p[0].lineno = p.lineno(0)

  def p_for_instruction(self, p):
    """FOR_INSTRUCTION : FOR ID ASSIGN RANGE INSTRUCTION"""
    p[0] = For(p[2], p[4], p[5])
    p[0].lineno = p.lineno(0)

  def p_break_instruction(self, p):
    """BREAK_INSTRUCTION : BREAK"""
    p[0] = Break()
    p[0].lineno = p.lineno(0)

  def p_continue_instruction(self, p):
    """CONTINUE_INSTRUCTION : CONTINUE"""
    p[0] = Continue()
    p[0].lineno = p.lineno(0)

  def p_return_instruction(self, p):
    """RETURN_INSTRUCTION : RETURN
                          | RETURN INNER_ARRAY"""
    if len(p) == 3:
      p[0] = Return(p[2])
    else:
      p[0] = Return()
    p[0].lineno = p.lineno(0)

  def p_print_instruction(self, p):
    """PRINT_INSTRUCTION : PRINT INNER_ARRAY"""
    p[0] = Print(p[2])
    p[0].lineno = p.lineno(0)
