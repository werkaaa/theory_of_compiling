
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

class Expression(Node):
  def __init__(self, type):
    super(Expression, self).__init__(type)

class Instructions(Node):
  def __init__(self, instructions, single_instruction):
    self.type = 'instructions'
    self.instructions = []
    if instructions:
      self.instructions += [instructions]
    if single_instruction:
      self.instructions += [single_instruction]

class NumberBinaryOperation(Expression):
  def __init__(self, left, operator, right):
    super(NumberBinaryOperation, self).__init__('NumberBinaryOperation')
    #self.type = 'NumberBinaryOperation'
    self.left = left
    self.operator = operator
    self.right = right

class MatrixBinaryOperation(Expression):
  def __init__(self, left, operator, right):
    super(MatrixBinaryOperation, self).__init__('MatrixBinaryOperation')
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
    super(IntNum, self).__init__('IntNum')
    self.value = int(value)

class FloatNum(Number):
  def __init__(self, value):
    super(FloatNum, self).__init__('FloatNum')
    self.value = float(value)

class Arrays(Node):
  def __init__(self, rows_list, last_row):
    super(Arrays, self).__init__('Arrays')
    self.rows = []
    if rows_list:
      self.rows += rows_list
    if last_row:
      self.rows += [last_row]

class Array(Node):
  def __init__(self, exprs, last_expr):
    super(Array, self).__init__('Array')
    self.exprs = []
    if exprs:
      self.exprs.extend(exprs.exprs)
    if last_expr:
      self.exprs.append(last_expr)

class BooleanExpression(Expression):
  def __init__(self, left, operator, right):
    super(BooleanExpression, self).__init__('BooleanExpression')
    self.left = left
    self.operator = operator
    self.right = right

class Transpose(Expression):
  def __init__(self, value):
    super(Transpose, self).__init__('Transpose')
    self.value = value

class Assignment(Expression):
  def __init__(self, left, operator, right):
    super(Assignment, self).__init__('Assignment')
    self.left = left
    self.operator = operator
    self.right = right

class String(Node):
  def __init__(self, value):
    super(String, self).__init__('String')
    self.value = value

class UnaryMinus(Expression):
  def __init__(self, value):
    super(UnaryMinus, self).__init__('UnaryMinus')
    self.value = value

class MatrixFunction(Expression):
  def __init__(self, function, parameter1, parameter2):
    super(MatrixFunction, self).__init__('MatrixFunction')
    self.function = function
    self.parameter1 = parameter1
    self.parameter2 = parameter2

