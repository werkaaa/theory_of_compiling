#!/usr/bin/python

import scanner
import ply.yacc as yacc

from ast import *

class Parser:
  tokens = scanner.Scanner().tokens

  precedence = (
    ("nonassoc", ':'),  ###
    ("nonassoc", 'ifx'),
    ("nonassoc", 'ELSE'),
    ("nonassoc", 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ("right", 'ASSIGN'),
    ("nonassoc", 'GREATER', 'GREATEREQ', 'SMALLER', 'SMALLEREQ', 'EQ', 'NOTEQ'),
    ("right", 'ID', 'STRING', '['), #### przemyslec
    ("left", 'ADD', 'SUB'),
    ("left", 'MUL', 'DIV'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", 'DOTMUL', 'DOTDIV'),
    ("right", 'UMINUS'),
    ("left", 'TRANSPOSE'),
  )

  start = 'program'

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
    """program : instructions_opt """
    p[0] = p[1]

  def p_empty(self, p):
    """empty : """
    pass

  def p_instructions_opt(self, p):
    """instructions_opt : instructions
                        | empty """
    p[0] = p[1]

  def p_block_of_instructions(self, p):
    """block : '{' instructions_opt '}' """
    p[0] = Block(p[2])
    p[0].lineno = p.lineno(0)

  def p_instructions(self, p):
    """instructions : instructions instruction
                    | instruction """
    if len(p) == 2:
      p[0] = Instructions(None, p[1])
    else:
      p[0] = Instructions(p[1], p[2])
    p[0].lineno = p.lineno(0)

  def p_instruction(self, p):
    """instruction : expression ';'
                   | assignment ';'
                   | if_instruction
                   | while_instruction
                   | for_instruction
                   | break_instruction ';'
                   | continue_instruction ';'
                   | return_instruction ';'
                   | print_instruction ';'
                   | block """
    p[0] = p[1]

  # Expressions
  def p_expression(self, p):
    """expression : number
                  | array
                  | variable
                  | STRING """
    if isinstance(p[1], str):
      p[0] = String(p[1])
    else:
      p[0] = p[1]

  def p_unary_minus(self, p):
    """expression : SUB expression %prec UMINUS """
    if len(p) == 3:
      p[0] = UnaryMinus(p[2])
    else:
      p[0] = UnaryMinus(p[3])
    p[0].lineno = p.lineno(0)

  def p_binary_operations(self, p):
    """expression : expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression """
    p[0] = NumberBinaryOperation(p[1], p[2], p[3])
    p[0].lineno = p.lineno(0)

  def p_binary_operations_dot(self, p):
    """expression : expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression """
    p[0] = MatrixBinaryOperation(p[1], p[2], p[3])
    p[0].lineno = p.lineno(0)

  def p_expression_par(self, p):
    """expression : '(' expression ')' """
    p[0] = p[2]
    p[0].lineno = p.lineno(0)

  def p_transpose(self, p):
    """expression : expression TRANSPOSE """
    p[0] = Transpose(p[1])
    p[0].lineno = p.lineno(0)

  def p_matrix_func_call(self, p):
    """expression : matrix_func '(' inner_array ')' """
    p[0] = MatrixFunction(p[1], p[3])
    p[0].lineno = p.lineno(0)

  def p_matrix_functions(self, p):
    """matrix_func : EYE
                   | ZEROS
                   | ONES """
    p[0] = p[1]

  # Numbers
  def p_int(self, p):
    """number : INTNUM """
    p[0] = IntNum(p[1])
    p[0].lineno = p.lineno(0)

  def p_float(self, p):
    """number : FLOATNUM """
    p[0] = FloatNum(p[1])
    p[0].lineno = p.lineno(0)

  # Arrays
  def p_array(self, p):
    """array : '[' inner_array ']'
             | '[' ']' """
    p[0] = p[2]

  def p_inner_array(self, p):
    """inner_array : expression ',' inner_array
                   | expression """
    if len(p)==2:
      p[0] = InnerList(p[1])
    else:
      p[0] = InnerList(p[1], p[3])
    p[0].lineno = p.lineno(0)

  def p_range_list_indices(self, p):
    """list_indices : range ',' list_indices
                    | range """
    if len(p)==2:
      p[0] = InnerList(p[1])
    else:
      p[0] = InnerList(p[1], p[3])

    p[0].lineno = p.lineno(0)

  def p_expression_list_indices(self, p):
    """list_indices : expression ',' list_indices
                    | expression """
    if len(p)==2:
      p[0] = InnerList(p[1])
    else:
      p[0] = InnerList(p[1], p[3])

    p[0].lineno = p.lineno(0)

  def p_variable(self, p):
    """variable : ID """
    p[0] = Identifier(p[1])
    p[0].lineno = p.lineno(0)

  def p_array_variable(self, p):
    """variable : ID '[' list_indices ']' """
    p[0] = ArrayElement(Identifier(p[1]), p[3])
    p[0].lineno = p.lineno(0)

  def p_string_variable(self, p):
    """variable : STRING '[' list_indices ']' """
    p[0] = ArrayElement(p[1], p[3])
    p[0].lineno = p.lineno(0)

  def p_binary_relations(self, p):
    """boolean_expression : expression SMALLER expression
                          | expression GREATER expression
                          | expression SMALLEREQ expression
                          | expression GREATEREQ expression
                          | expression NOTEQ expression
                          | expression EQ expression
                          | expression """
    if len(p) == 2:
      p[0] = p[1]  # Expression as a relation value
    else:
      p[0] = BooleanExpression(p[1], p[2], p[3])
    p[0].lineno = p.lineno(0)

  def p_assignment(self, p):
    """assignment : variable ASSIGN expression
                  | variable ADDASSIGN expression
                  | variable SUBASSIGN expression
                  | variable MULASSIGN expression
                  | variable DIVASSIGN expression """
    p[0] = Assignment(p[1], p[2], p[3])
    p[0].lineno = p.lineno(0)

  def p_if_else_instruction(self, p):
    """if_instruction : IF '(' boolean_expression ')' instruction %prec ifx
                      | IF '(' boolean_expression ')' instruction ELSE instruction """
    if len(p) == 6:
      p[0] = If(p[3], p[5], None)
    else:
      p[0] = If(p[3], p[5], p[7])
    p[0].lineno = p.lineno(0)

  def p_while_instruction(self, p):
    """while_instruction : WHILE '(' boolean_expression ')' instruction """
    p[0] = While(p[3], p[5])
    p[0].lineno = p.lineno(0)

  def p_range(self, p):
    """range : expression ':' expression """
    p[0] = Range(p[1], p[3])
    p[0].lineno = p.lineno(0)

  def p_for_instruction(self, p):
    """for_instruction : FOR ID ASSIGN range instruction """
    p[0] = For(p[2], p[4], p[5])
    p[0].lineno = p.lineno(0)

  def p_break_instruction(self, p):
    """break_instruction : BREAK """
    p[0] = Break()
    p[0].lineno = p.lineno(0)

  def p_continue_instruction(self, p):
    """continue_instruction : CONTINUE """
    p[0] = Continue()
    p[0].lineno = p.lineno(0)

  def p_return_instruction(self, p):
    """return_instruction : RETURN
                          | RETURN inner_array """
    if len(p) == 3:
      p[0] = Return(p[2])
    else:
      p[0] = Return()
    p[0].lineno = p.lineno(0)

  def p_print_instruction(self, p):
    """print_instruction : PRINT inner_array """
    p[0] = Print(p[2])
    p[0].lineno = p.lineno(0)
