class Node:
  def __init__(self, type, children=None, leaf=None):
    self.type = type
    if children:
      self.children = children
    else:
      self.children = []
    self.leaf = leaf

class Instruction(Node):
  def __init__(self):
    super(Instruction, self).__init__()

class Expression(Instruction):
  def __init__(self):
    super(Expression, self).__init__()

class If(Instruction):
  def __init__(self, condition, if_block, else_block):
    self.type = 'IF'
    self.condition = condition
    self.if_block = if_block
    self.else_block = else_block

class While(Instruction):
  def __init__(self, condition, block):
    self.type = 'WHILE'
    self.condition = condition
    self.block = block

class For(Instruction):
  def __init__(self, variable, range, block):
    self.type = 'FOR'
    self.variable = variable
    self.range = range
    self.block = block

class Range(Node):
  def __init__(self, start_value, end_value):
    self.type = 'RANGE'
    self.start_value = start_value
    self.end_value = end_value

class Break(Instruction):
  def __init__(self):
    self.type = 'BREAK'

class Continue(Instruction):
  def __init__(self):
    self.type = 'CONTINUE'

class Return(Instruction):
  def __init__(self, arg=None):
    self.type = 'RETURN'
    self.arg = arg

class Print(Instruction):
  def __init__(self, arg=None):
    self.type = 'PRINT'
    self.arg = arg

class Instructions(Node):
  def __init__(self, instructions, single_instruction):
    self.type = 'INSTRUCTIONS'
    self.instructions = []
    if instructions:
      self.instructions += [instructions]
    if single_instruction:
      self.instructions += [single_instruction]

class NumberBinaryOperation(Expression):
  def __init__(self, left, operator, right):
    self.type = 'NUMBER_BINARY_OPERATION'
    self.left = left
    self.operator = operator
    self.right = right

class MatrixBinaryOperation(Expression):
  def __init__(self, left, operator, right):
    self.type = 'MATRIX_BINARY_OPERATION'
    self.left = left
    self.operator = operator
    self.right = right

class Variable(Expression):
  pass

class Identifier(Variable):
  def __init__(self, name):
    self.type = 'ID'
    self.name = name

class Number(Expression):
  def __init__(self, type):
    super(Number, self).__init__(type)

class IntNum(Number):
  def __init__(self, value):
    self.type = 'INTNUM'
    self.value = int(value)

class FloatNum(Number):
  def __init__(self, value):
    self.type = 'FLOATNUM'
    self.value = float(value)

class BooleanExpression(Expression):
  def __init__(self, left, operator, right):
    self.type = 'BOOLEAN_EXPRESSION'
    self.left = left
    self.operator = operator
    self.right = right

class Transpose(Expression):
  def __init__(self, value):
    self.type = 'TRANSPOSE'
    self.value = value

class Assignment(Expression):
  def __init__(self, left, operator, right):
    self.type = 'ASSIGNMENT'
    self.left = left
    self.operator = operator
    self.right = right

class String(Node):
  def __init__(self, value):
    self.type = 'STRING'
    self.value = value

class UnaryMinus(Expression):
  def __init__(self, value):
    self.type = 'UNARY_MINUS'
    self.value = value

class MatrixFunction(Expression):
  def __init__(self, function, parameter1, parameter2):
    self.type = 'MATRIX_FUNCTION'
    self.function = function
    self.parameter1 = parameter1
    self.parameter2 = parameter2

class Block(Instruction):
  def __init__(self, instructions):
    self.type = 'INSTRUCTIONS_BLOCK'
    self.instructions = instructions

class ArrayElement(Instruction):
  def __init__(self, array, ids):
    self.type = 'ARRAY_ELEMENT'
    self.array = array
    self.ids = ids


class InnerList(Node):
  def __init__(self, new_element, elements=None):
    self.type = 'list'
    self.elements = []
    if elements:
      self.elements = elements.elements

    self.elements.append(new_element)

