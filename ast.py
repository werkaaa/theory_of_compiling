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

