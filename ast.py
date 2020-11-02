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
  def __init__(self):
    super(Expression, self).__init__()

class BinOp(Expression):
  def __init__(self):
    super(BinOp, self).__init__()

class BinOpNum(BinOp):
  def __init__(self, left, op, right):
    super(BinOpNum, self).__init__()
    self.type = 'bin_op_num'
    self.left = left
    self.right = right
    self.op = op


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


