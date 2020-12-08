import ast
from symbol_table import SymbolTable

TYPE_MAP = {
  'INTNUM':
    {
      'FLOATNUM': 'FLOATNUM',
      'INTNUM': 'INTNUM'
    },
  'FLOATNUM':
    {
      'FLOATNUM': 'FLOATNUM',
      'INTNUM': 'FLOATNUM'
    }
}

class NodeVisitor(object):

  def visit(self, node):
    method = 'visit_' + node.__class__.__name__
    visitor = getattr(self, method, self.generic_visit)
    if not hasattr(node, 'in_type'):
      node.in_type = visitor(node)
    return node.in_type


  def generic_visit(self, node):
    print(node)
    if isinstance(node, list):
      for elem in node:
        self.visit(elem)

class TypeChecker(NodeVisitor):

  def visit_Program(self, node):
    self.symbol_table = SymbolTable('program', 'program_table')
    self.visit(node.instructions_opt)
    return node.type

  def variable_declared(self, node):
    if self.symbol_table.get(node.name) is None:
      print((f'ERROR in line {node.lineno}\n'
             f'{node.name} is not declared\n'))
      return False
    return True

  def visit_Block(self, node):
    self.visit(node.instructions)
    node.in_type = node.type
    return node.in_type

  def visit_Assignment(self, node):
    # print('assignment')
    # right = node.right
    # left = node.left
    # type_left = self.visit(left)
    # type_right = self.visit(right)
    #
    # error_encountered = False
    # if type_right == 'ID':
    #   if self.variable_declared(right):
    #     right = self.symbol_table.get(right.name)
    #     type_right = self.visit(right)
    #   else:
    #     error_encountered = True
    #
    # if type_right == 'error':
    #   error_encountered = True
    # elif type_right not in ['array_element', 'INTNUM', 'FLOATNUM',
    #                         'array', 'STRING',
    #                         'TRANSPOSE', 'unary_minus', 'matrix_binary_operation'
    #                         'number_binary_operation', 'boolean_expression']:
    #   print((f'ERROR in line {node.lineno}\n'
    #          f'{type_right} is not a valid type '
    #          'for the right side of assignmet\n'))
    #   error_encountered = True
    #
    # if type_left not in ['ID', 'array_element']:
    #   print((f'ERROR in line {node.lineno}\n'
    #          f'Cannot assign to {type_left}\n'))
    #   error_encountered = True
    #
    #
    # if (node.operator != '=' and
    #     type_left == 'ID' and
    #     self.variable_declared(node.left)):
    #
    # #if not error_encountered:
    # self.symbol_table.put(node.left.name, node.right)
    #   # print(self.symbol_table.table)
    # return node.type
    # TODO: Skoro nie potrzebujemy odrzucać nieporawnie zadeklarowanych zmiennych z tablicy
    #  symboli, tę funkcję można mocno uprościć. Mógłbys się upewnić, że na pewno nie potrzebujemy
    #  odrzucac takich zmiennych?
    print('assignment')
    right = node.right
    left = node.left
    type_left = self.visit(left)
    type_right = self.visit(right)

    if type_right == 'ID':
      if self.variable_declared(right):
        right = self.symbol_table.get(right.name)
        type_right = self.visit(right)

    elif type_right not in ['array_element', 'INTNUM', 'FLOATNUM', 'array', 'STRING',
                            'TRANSPOSE', 'unary_minus', 'matrix_binary_operation',
                            'number_binary_operation', 'boolean_expression']:
      print((f'ERROR in line {node.lineno}\n'
             f'{type_right} is not a valid type '
             'for the right side of assignmet\n'))

    if type_left not in ['ID', 'array_element']:
      print((f'ERROR in line {node.lineno}\n'
             f'Cannot assign to {type_left}\n'))

    # TODO: assignment to array slicing and array indices jeśli do
    #  slicingu to wymiary muszą się zgadzać


    if (node.operator != '=' and
        type_left == 'ID' and
        self.variable_declared(node.left)):
      #TODO: sprawdzać typy przy -=, +=, ...
      pass

    self.symbol_table.put(node.left.name, node.right)

    return node.type

  def visit_For(self, node):
    self.visit(node.variable)
    self.visit(node.range)
    self.symbol_table.push_scope('loop')
    self.symbol_table.put_local(node.variable, ast.IntNum(node.range.start_value))
    self.visit(node.instruction)
    self.symbol_table.pop_scope()
    return node.type

  def visit_While(self, node):
    self.visit(node.condition)
    self.symbol_table.push_scope('loop')
    self.visit(node.instruction)
    self.symbol_table.pop_scope()
    return node.type

  def visit_If(self, node):
    self.visit(node.condition)
    self.symbol_table.push_scope('if')
    self.visit(node.if_block)
    self.symbol_table.pop_scope()
    if node.else_block is not None:
      self.symbol_table.push_scope('else')
      self.visit(node.if_block)
      self.symbol_table.pop_scope()

    return self.type

  def visit_Break(self, node):
    if not self.symbol_table.get_scope() == 'loop':
      print((f'ERROR in line {node.lineno}\n'
             f'Cannot break from current scope\n'))

    return node.type

  def visit_Continue(self, node):
    if not self.symbol_table.get_scope() == 'loop':
      print((f'ERROR in line {node.lineno}\n'
             f'Cannot continue in current scope\n'))

    return node.type

  def visit_Return(self, node):
    if node.args is not None:
      self.visit(node.args)
    return node.type

  def visit_Print(self, node):
    self.visit(node.args)
    return node.type

  def visit_ArrayElement(self, node):
    self.variable_declared(node.array)
    self.visit(node.ids)
    # TODO: slicing - trzeba uwzględnić
    #  trzeba z listIndex przekazać jakoś min i max zakres, żeby wiedzieć
    #  czy nie sięgamy poza rozmiar array, należałoby też sprawdzić czy to
    #  wgl jest array
    # TODO: fajnie gdyby to zwracało typ elementu, lub array (wtedy node
    #  z rozmiarem!) jeśli zastosowany był slicing, jeśli wystąpi bląd to node.type
    return node.type

  # Expressions
  def visit_IntNum(self, node):
    return node.type

  def visit_FloatNum(self, node):
    return node.type

  def visit_String(self, node):
    return node.type

  def visit_Array(self, node):
    self.visit(node.list)
    node.num_rows = node.list.num_rows
    node.num_cols = node.list.num_cols
    return node.type

  def visit_NumberBinaryOperation(self, node):
    print('number_bin_op')
    expr_left = node.left
    expr_right = node.right

    type_left = self.visit(expr_left)
    type_right = self.visit(expr_right)
    if type_left == 'ID':
      if not self.variable_declared(node.left):
        type_left = 'unknown'
      else:
        expr_left = self.symbol_table.get(node.left.name)
        type_left = self.visit(expr_left)

    if type_right == 'ID':
      if not self.variable_declared(node.right):
        type_right = 'unknown'
      else:
        expr_right = self.symbol_table.get(node.right.name)
        type_right = self.visit(expr_right)

    if (type_left in ['unknown', 'number_binary_operation', 'unary_minus'] or
        type_right in ['unknown', 'number_binary_operation', 'unary_minus']):
      return node.type

    if (type_left in ['array', 'matrix_function', 'TRANSPOSE', 'matrix_binary_operation'] and
       type_right in ['array', 'matrix_function', 'TRANSPOSE', 'matrix_binary_operation']):
    #if type_left == 'array' and type_right  == 'array':

      if node.operator == '*':
        if (expr_left.num_cols != 'unknown' and
            expr_right.num_rows != 'unknown' and
            expr_left.num_cols != expr_right.num_rows):

          print((f'ERROR in line {node.lineno}\n'
                 f'Inconsistent shape. Cannot {node.operator} '
                 f'matrices of shape {expr_left.num_rows}x{expr_left.num_cols} '
                 f'and {expr_right.num_rows}x{expr_right.num_cols}\n'))
          node.num_rows = expr_left.num_rows
          node.num_cols = expr_right.num_cols
          return 'matrix_binary_operation'
        else:
          node.num_rows = expr_left.num_rows
          node.num_cols = expr_right.num_cols
          return 'array'
      else:
        print((f'ERROR in line {node.lineno}\n'
               f'Operation {node.operator} not supported between {type_left} '
               f'and {type_right}\n'))
        return node.type
    elif type_left in ['FLOATNUM', 'INTNUM'] and type_right in ['FLOATNUM', 'INTNUM']:
      node.value = 'unknown'
      return TYPE_MAP[type_left][type_right]
    elif type_left == 'STRING' and type_right == 'STRING' and node.operator == '+':
      return 'STRING'


    print(expr_left)
    print((f'ERROR in line {node.lineno}\n'
           f'Operation {node.operator} not supported between {type_left} '
           f'and {type_right}\n'))

    return node.type

  def visit_MatrixBinaryOperation(self, node):
    """If successful will return 'array' type if not successful will return
    'matrix_binary_operation'. Either way, the node will have num_rows, num_cols
    attributes, which may be ste to unknown.
    """
    print('number_bin_op')
    expr_left = node.left
    expr_right = node.right

    type_left = self.visit(expr_left)
    type_right = self.visit(expr_right)
    if type_left == 'ID':
      if not self.variable_declared(node.left):
        type_left = 'unknown'
      else:
        expr_left = self.symbol_table.get(node.left.name)
        type_left = self.visit(expr_left)

    if type_right == 'ID':
      if not self.variable_declared(node.right):
        type_right = 'unknown'
      else:
        expr_right = self.symbol_table.get(node.right.name)
        type_right = self.visit(expr_right)

    # if (type_left in ['unknown', 'number_binary_expression'] or
    #     type_right in ['unknown', 'number_binary_expression']):

    if type_left == 'unknown' or type_right == 'unknown':
      node.num_rows = 'unknown'
      node.num_cols = 'unknown'
      return node.type

    if (type_left in ['array', 'matrix_function', 'TRANSPOSE', 'matrix_binary_expression'] and
       type_right in ['array', 'matrix_function', 'TRANSPOSE', 'matrix_binary_expression']):

      if expr_left.num_rows == 'unknown' or expr_right.num_rows == 'unknown':
        num_rows = 'unknown'
      else:
        num_rows = expr_left.num_rows

      if expr_left.num_cols == 'unknown' or expr_right.num_cols == 'unknown':
        num_cols = 'unknown'
      else:
        num_cols = expr_left.num_cols

      if ((num_cols != 'unknown' and expr_right.num_cols != expr_left.num_cols) or
          (num_rows != 'unknown' and expr_right.num_rows != expr_left.num_rows)):
        print((f'ERROR in line {node.lineno}\n'
               f'Inconsistent shape. Cannot {node.operator} '
               f'matrices of shape {expr_left.num_rows}x{expr_left.num_cols} '
               f'and {expr_right.num_rows}x{expr_right.num_cols}\n'))
        node.num_rows = 'unknown'
        node.num_cols = 'unknown'
        return node.type
      else:
        node.num_rows = num_rows
        node.num_cols = num_cols
        return 'array'

    print(expr_left)
    print((f'ERROR in line {node.lineno}\n'
           f'Operation {node.operator} not supported between {type_left} '
           f'and {type_right}\n'))

    node.num_rows = 'unknown'
    node.num_cols = 'unknown'
    return node.type

  def visit_BooleanExpression(self, node):
    print('boolean_exp')
    expr_left = node.left
    expr_right = node.right

    type_left = self.visit(expr_left)
    type_right = self.visit(expr_right)
    if type_left == 'ID':
      if not self.variable_declared(node.left):
        type_left = 'unknown'
      else:
        expr_left = self.symbol_table.get(node.left.name)
        type_left = self.visit(expr_left)

    if type_right == 'ID':
      if not self.variable_declared(node.right):
        type_right = 'unknown'
      else:
        expr_right = self.symbol_table.get(node.right.name)
        type_right = self.visit(expr_right)

    if (type_left in ['unknown', 'number_binary_expression'] or
        type_right in ['unknown', 'number_binary_expression']):
      return node.type
    print(type_left, type_right)
    if ((type_left in ['FLOATNUM', 'INTNUM'] and
         type_right in ['FLOATNUM', 'INTNUM']) or
        (type_left == 'STRING' and type_right == 'STRING')):
      return node.type

    print(expr_left)
    print((f'ERROR in line {node.lineno}\n'
           f'Operator {node.operator} not supported between {type_left} '
           f'and {type_right}\n'))

    return node.type

  def visit_MatrixFunction(self, node):
    parameters = node.parameter
    self.visit(parameters)
    if parameters.num_rows != 1 and parameters.num_cols > 2:
      print((f'ERROR in line {node.lineno}\n'
             f'{parameters} are not valid matrix function arguments\n'))
    parameter = parameters.elements[0]
    parameter_type = self.visit(parameter)
    if parameter_type == 'ID':
      if self.variable_declared(parameter):
        parameter = self.symbol_table.get(parameter.name)
        parameter_type = self.visit(parameter)
      else:
        node.num_rows = 'unknown'
    if parameter_type == 'INTNUM':
      node.num_rows = parameter.value
    else:
      print((f'ERROR in line {node.lineno}\n'
             f'Matrix function {node.function} cannot take '
             f'{parameter} as parameter\n'))
      node.num_rows = 'unknown'
    if parameters.num_cols == 2:
      parameter = parameters.elements[1]
      parameter_type = self.visit(parameter)
      if parameter_type == 'ID':
        if self.variable_declared(parameter):
          parameter = self.symbol_table.get(parameter.name)
          parameter_type = self.visit(parameter)
        else:
          node.num_cols = 'unknown'
      if parameter_type == 'INTNUM':
        node.num_cols = parameter.value
      else:
        print((f'ERROR in line {node.lineno}\n'
               f'Matrix function {node.function} cannot take '
               f'{node.parameter} as parameter\n'))
        node.num_cols = 'unknown'
    else:
      node.num_cols = node.num_rows

    return 'array'

  def visit_UnaryMinus(self, node):
    value = node.value
    value_type = self.visit(value)
    if value_type == 'ID':
      if not self.variable_declared(value):
        value_type = 'unary_minus'
      else:
        value = self.symbol_table.get(value.name)
        value_type = self.visit(value)

    if value_type == 'STRING':
      print((f'ERROR in line {node.lineno}\n'
             'Cannot place unary minus before STRING\n'))
    elif value_type == 'array':
      node.num_cols = value.num_cols
      node.num_rows = value.num_rows

    return value_type

  def visit_Transpose(self, node):
    value = node.value
    value_type = self.visit(value)
    if value_type == 'ID':
      if not self.variable_declared(value):
        value_type = 'unknown'
      else:
        value = self.symbol_table.get(value.name)
        value_type = self.visit(value)

    if value_type in ['array', 'matrix_function', 'TRANSPOSE', 'matrix_binary_operation']:
    #if value_type == 'array':
      node.num_cols = value.num_rows
      node.num_rows = value.num_cols
    else:
      print((f'ERROR in line {node.lineno}\n'
             f'Cannot transpose {value_type}\n'))
      value_type = 'TRANSPOSE'
      node.num_cols = 'unknown'
      node.num_rows = 'unknown'

    return value_type

  # Other
  def visit_Identifier(self, node):
    return node.type

  def visit_Range(self, node):
    start_value = node.start_value
    end_value = node.end_value
    start_type = self.visit(start_value)
    end_type = self.visit(end_value)

    if start_type == 'ID':
      if not self.variable_declared(start_value):
        start_type = 'unknown'
      else:
        start_value = self.symbol_table.get(start_value.name)
        start_type = self.visit(start_value)

    if start_type == 'ID':
      if not self.variable_declared(end_value):
        end_type = 'unknown'
      else:
        end_value = self.symbol_table.get(end_value.name)
        end_type = self.visit(end_value)

    if not start_type in ['INTNUM', 'array_element', 'unknown']:
      print((f'ERROR in line {node.lineno}\n'
             f'{start_type} is not a valid type for a range start\n'))

    if not end_type in ['INTNUM', 'array_element', 'unknown']:
      print((f'ERROR in line {node.lineno}\n'
             f'{end_type} is not a valid type for a range start\n'))

    return node.type

  def visit_InnerList(self, node):
    first_elem = node.elements[0]
    first_elem_type = self.visit(first_elem)
    #TODO: może tu wykluczyć jeszcze jakieś typy?
    for elem in node.elements[1:]:
      elem_type = self.visit(elem)
      if elem_type != first_elem_type:
        print((f'ERROR in line {node.lineno}\n'
               f'Inconsistent types {first_elem_type} and {elem_type} in the array\n'))
        break
      elif first_elem_type == 'array' and first_elem.num_cols != elem.num_cols:
        print((f'ERROR in line {node.lineno}\n'
               f'Inconsistent shapes {first_elem.num_cols} and {elem.num_cols} in the array\n'))
        break
    # TODO: wykluczyć więcej niż 2 wymiary
    if first_elem_type == 'array':
      node.num_cols = first_elem.num_cols
      node.num_rows = len(node.elements)
    else:
      node.num_rows = 1
      node.num_cols = len(node.elements)

    return node.type

  def visit_ListOfIndices(self, node):
    for elem in node.elements:
      elem_type = self.visit(elem)
      if elem_type == 'ID':
        if not self.variable_declared(elem):
          elem_type = 'unknown'
        else:
          elem = self.symbol_table.get(elem.name)
          elem_type = self.visit(elem)

      if not elem_type in ['INTNUM', 'RANGE', 'unknown']:
        print((f'ERROR in line {node.lineno}\n'
               f'{elem_type} is not a valid array index type\n'))
        break

    return node.type

  def visit_ListOfArguments(self, node):
    for elem in node.elements:
      self.visit(elem)
      if elem.type == 'ID':
        self.variable_declared(elem)
    return node.type

  def visit_Instructions(self, node):
    for elem in node.elements:
      self.visit(elem)
    return node.type


# TODO: numery linii coś nie działają
# TODO: potestować ile się da