from ast import *
import symbol_table
from memory import *
from exceptions import  *
from visit import *
import numpy as np
import operator as op
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):

    def __init__(self):
      self.memory_stack = MemoryStack()
      self.operators = {
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '.+': op.add,
        '.-': op.sub,
        '.*': op.mul,
        './': op.truediv,
      }

    @on('node')
    def visit(self, node):
        pass

    # Instructions
    @when(Block)
    def visit(self, node):
      self.visit(node.instructions)

    @when(Assignment)
    def visit(self, node):
      right = self.visit(node.right)

      if len(node.operator) == 2:
        left = self.visit(node.left)
        right = self.operators[node.operator[0]](left, right)

      if isinstance(node.left, Identifier):
        self.memory_stack.insert(node.left.name, right)

      #TODO: slicing przy assignment


    @when(For)
    def visit(self, node):
      self.memory_stack.push('for_loop')
      loop_range = self.visit(node.range)
      for i in loop_range:
        self.memory_stack.insert(node.variable.name, i)
        try:
          self.visit(node.instruction)
        except BreakException:
          break
        except ContinueException:
          pass
      self.memory_stack.pop()


    @when(While)
    def visit(self, node):
      self.memory_stack.push('while_loop')
      while self.visit(node.condition):
        try:
          self.visit(node.instruction)
        except BreakException:
          break
        except ContinueException:
          pass
      self.memory_stack.pop()

    @when(If)
    def visit(self, node):
      self.memory_stack.push('if')
      if self.visit(node.condition):
        self.visit(node.if_block)
      elif node.else_block is not None:
        self.visit(node.else_block)
      self.memory_stack.pop()

    @when(Break)
    def visit(self, node):
      raise BreakException

    @when(Continue)
    def visit(self, node):
      raise ContinueException

    @when(Return)
    def visit(self, node):
      raise ReturnValueException(node.args)

    @when(Print)
    def visit(self, node):
      visited_args = self.visit(node.args)
      print(', '.join([str(arg) for arg in visited_args]))

    @when(ArrayElement)
    def visit(self, node):
      # TODO: tu zapewne trzeba będzie pokombinować jak ostatnio ze slicingiem
      array = self.visit(node.array)
      ids = self.visit(node.ids)
      return array[ids]

    # Expressions
    @when(IntNum)
    def visit(self, node):
      return node.value

    @when(FloatNum)
    def visit(self, node):
      return node.value

    @when(String)
    def visit(self, node):
      return node.value

    @when(Array)
    def visit(self, node):
      return np.array(self.visit(node.list))

    @when(NumberBinaryOperation)
    def visit(self, node):
      left = self.visit(node.left)
      right = self.visit(node.right)

      if isinstance(left, np.ndarray) and isinstance(right, np.ndarray) and node.operator == '*':
        return left @ right

      return self.operators[node.operator](left, right)

    @when(MatrixBinaryOperation)
    def visit(self, node):
      left = self.visit(node.left)
      right = self.visit(node.right)
      return self.operators[node.operator](left, right)

    @when(BooleanExpression)
    def visit(self, node):
      #TODO boolean expression
      pass

    @when(MatrixFunction)
    def visit(self, node):
      parameter = self.visit(node.parameter)
      num_rows = parameter[0]
      num_cols = parameter[1] if len(parameter) > 1 else None
      if node.function == 'eye':
        return np.eye(num_rows)
      elif node.function == 'ones':
        if num_cols is not None:
          return np.ones((num_rows, num_cols))
        else:
          return np.ones(num_rows)
      elif node.function == 'zeros':
        if num_cols is not None:
          return np.zeros((num_rows, num_cols))
        else:
          return np.zeros(num_rows)

    @when(UnaryMinus)
    def visit(self, node):
      return -self.visit(node.value)

    @when(Transpose)
    def visit(self, node):
      return self.visit(node.value).T

    # Other
    @when(Program)
    def visit(self, node):
      self.visit(node.instructions_opt)

    @when(Identifier)
    def visit(self, node):
      return self.memory_stack.get(node.name)

    @when(Range)
    def visit(self, node):
      start_value = self.visit(node.start_value)
      end_value = self.visit(node.end_value)
      return range(start_value, end_value)

    @when(InnerList)
    def visit(self, node):
      visited_list = []
      for element in node.elements:
        element = self.visit(element)
        visited_list.append(element)
      return visited_list

    @when(ListOfIndices)
    def visit(self, node):
      visited_list = []
      for element in node.elements:
        element = self.visit(element)
        visited_list.append(element)
      return visited_list

    @when(ListOfArguments)
    def visit(self, node):
      visited_list = []
      for element in node.elements:
        element = self.visit(element)
        visited_list.append(element)
      return visited_list

    @when(Instructions)
    def visit(self, node):
      for element in node.elements:
        self.visit(element)

#TODO W mainie trzeba zmienić, żeby interpreter odpalał się wtw gdy nie ma syntax error i type_checker odpalił sie poprawnie
# pewnie wystarczy do tego jakaś flaga, która zmienia się w razie błędu (może specjalna funkcja w type_checker która printuje treść błędu i ustawia correct na False?

#TODO ustawianie typu elementu w matrix binary operation w type_checker gdy zwraca ona array lub matrix binary operation z użyciem
# słownika (to co pisałam dzisiaj)

#TODO potestować zwłaszcza na przykładach prowadzącego