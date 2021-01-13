from . import ast
from .symbol_table import SymbolTable
from collections import defaultdict


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        if not hasattr(node, 'in_type'):
            node.in_type = visitor(node)
        return node.in_type

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)


# noinspection PyPep8Naming
class TypeChecker(NodeVisitor):
    TYPE_MAP = None
    GOT_ERROR = False

    def __init__(self):
        # Attributes
        self.symbol_table = None
        self.loop_scopes_cnt = 0

        TypeChecker.initialize_type_dict()

    def get_type(self, *args):
        """ Obtain inferred type from the dictionary.

            There are several types of possible usage:
            - NumberBinaryOperation
                & MatrixBinaryOperation
                & BooleanExpression:
              get_type(op, type_left, type_right)
              Simply get the inferred type from dict.
              In BooleanExpression the op is just 'bool'.
            - Assign:
              get_type(op, type_left, type_right, detailed_type_left)
              type_left is either ID or array_element. detailed_type_left is
              more precise type of left operand f.e. if type_left was ID,
              detailed_type_left could be the type of variable (like INTNUM),
              having this ID.
    """

        result_type = self.TYPE_MAP[args[0]]
        for arg in args[1:]:
            if type(result_type) in [dict, defaultdict]:
                result_type = result_type[arg]
            else:
                break
        return result_type

    # noinspection PyTypeChecker,PyUnresolvedReferences
    @classmethod
    def initialize_type_dict(cls):
        if cls.TYPE_MAP:
            return
        else:
            cls.TYPE_MAP = defaultdict(lambda: 'unknown')

        # Available operations for '+', '-', '/'
        default_num_binop = defaultdict(lambda: 'number_binary_operation',
          {
            'INTNUM'   : defaultdict(lambda: 'error_op_not_sup',
              {
                'INTNUM'   : 'INTNUM',
                'FLOATNUM' : 'FLOATNUM',
                'unknown'  : 'unknown'
              }),
            'FLOATNUM' : defaultdict(lambda: 'error_op_not_sup',
              {
                'INTNUM'   : 'FLOATNUM',
                'FLOATNUM' : 'FLOATNUM',
                'unknown' : 'unknown',
              }),

            'array'                     : defaultdict(lambda: 'error_op_not_sup'),
            'TRANSPOSE'                 : defaultdict(lambda: 'error_op_not_sup'),
            'matrix_binary_operation'   : defaultdict(lambda: 'error_op_not_sup'),
            'STRING'                    : defaultdict(lambda: 'error_op_not_sup'),
            'unknown'                   : 'unknown',
          })

        matrix_mul_dict = defaultdict(lambda: 'error_op_not_sup',
          {
            'array'                    : 'array',
            'TRANSPOSE'                : 'array',
            'matrix_binary_operation'  : 'array',
          })

        # Number Subtraction
        cls.TYPE_MAP['-'] = default_num_binop

        # Number Division
        cls.TYPE_MAP['/'] = default_num_binop

        # Number Addition
        cls.TYPE_MAP['+'] = default_num_binop.copy()
        cls.TYPE_MAP['+']['STRING']['STRING'] = 'STRING'

        # Number Multiplication
        cls.TYPE_MAP['*'] = default_num_binop.copy()
        cls.TYPE_MAP['*']['STRING'] = defaultdict(lambda: 'error_op_not_sup',
                                                  {
                                                      'INTNUM': 'STRING',
                                                  })
        cls.TYPE_MAP['*']['INTNUM']['STRING'] = 'STRING'
        cls.TYPE_MAP['*']['array']                   = matrix_mul_dict
        cls.TYPE_MAP['*']['matrix_function']         = matrix_mul_dict
        cls.TYPE_MAP['*']['TRANSPOSE']               = matrix_mul_dict
        cls.TYPE_MAP['*']['matrix_binary_operation'] = matrix_mul_dict

        left_mat_op = defaultdict(lambda: 'matrix_binary_operation',
          {
            'array': 'array',
            'matrix_function': 'array',
            'TRANSPOSE': 'array',
            'matrix_binary_operation': 'array',
          })

        default_mat_op = defaultdict(lambda: 'matrix_binary_operation',
          {
            'array':                   left_mat_op,
            'matrix_function':         left_mat_op,
            'TRANSPOSE':               left_mat_op,
            'matrix_binary_operation': left_mat_op,
          })

        # Matrix Operations
        cls.TYPE_MAP['.+'] = default_mat_op
        cls.TYPE_MAP['.-'] = default_mat_op
        cls.TYPE_MAP['.*'] = default_mat_op
        cls.TYPE_MAP['./'] = default_mat_op

        assignable_types = [
          'ID',
          'INTNUM',
          'FLOATNUM',
          'array',
          'STRING',
          'TRANSPOSE',
          'unary_minus',
          'matrix_binary_operation',
          'number_binary_operation',
          'unknown',
          'array_element',
        ]

        array_assignment_dict = defaultdict(lambda : 'error_op_not_sup',
          {
            'array' : 'array',
            'TRANSPOSE': 'array',
            'unary_minus' : 'array',
            'matrix_binary_operation' : 'array',
          })

        assign_map = defaultdict(lambda : 'error_left_invalid',
          {
            'ID' : defaultdict(lambda : 'error_right_invalid',
              {key : 'ASSIGN' for key in assignable_types}),
            'array_element' : defaultdict(lambda : 'error_right_invalid',
              {
                # Unknown
                'unknown' : 'unknown',
                'array_element' : 'unknown',
                # Numbers
                'INTNUM' : defaultdict(lambda : 'error_op_not_sup',
                  {
                    'INTNUM' : 'INTNUM',
                    'FLOATNUM' : 'FLOATNUM',
                    'number_binary_operation' : 'unknown',
                    'unknown' : 'unknown',
                  }),
                'FLOATNUM' : defaultdict(lambda : 'error_op_not_sup',
                  {
                    'INTNUM' : 'FLOATNUM',
                    'FLOATNUM' : 'FLOATNUM',
                    'number_binary_operation' : 'unknown',
                    'unknown' : 'unknown',
                  }),
                'number_binary_operation' : defaultdict(lambda : 'error_op_not_sup',
                  {
                    'INTNUM' : 'INTNUM',
                    'FLOATNUM' : 'FLOATNUM',
                    'number_binary_operation' : 'unknown',
                    'unknown' : 'unknown',
                  }),
                # Arrays
                'array' :                   array_assignment_dict,
                'TRANSPOSE':                array_assignment_dict,
                'unary_minus' :             array_assignment_dict,
                'matrix_binary_operation' : array_assignment_dict,
                # String
                'STRING' : defaultdict(lambda : 'error_op_not_sup',
                  {
                    'STRING' : 'STRING',
                    'unknown' : 'unknown',
                  }),
              })
          })

        # Assignment
        cls.TYPE_MAP['='] = assign_map

        num_op_assign_map = defaultdict(lambda : 'error_op_not_sup',
          {
            'FLOATNUM' : 'ASSIGN',
            'INTNUM' : 'ASSIGN',
            'number_binary_operation' : 'ASSIGN',
          })

        op_assign_id_map = defaultdict(lambda : 'error_right_invalid',
          {
            'unknown' :                 'ASSIGN',
            'FLOATNUM' :                num_op_assign_map,
            'INTNUM' :                  num_op_assign_map,
            'number_binary_operation' : num_op_assign_map,
            'STRING' :                  'error_op_not_sup',
            'array' :                   'error_op_not_sup',
            'TRANSPOSE' :               'error_op_not_sup',
            'unary_minus' :             'error_op_not_sup',
            'matrix_binary_operation' : 'error_op_not_sup',
          })

        op_assign_map = defaultdict(lambda : 'error_left_invalid',
          {
            'ID' : op_assign_id_map.copy(),

            'array_element' : defaultdict(lambda : 'error_right_invalid',
              {
                # Unknown
                'unknown' : 'unknown',
                # Numbers
                'INTNUM' : defaultdict(lambda : 'error_op_not_sup',
                  {
                    # Here INTNUM (and others) means intnum or array of type intnum
                    'INTNUM' : 'INTNUM',
                    'FLOATNUM' : 'FLOATNUM',
                    'number_binary_operation' : 'unknown',
                    'unknown' : 'unknown',
                  }),
                'FLOATNUM' : defaultdict(lambda : 'error_op_not_sup',
                  {
                    'INTNUM' : 'FLOATNUM',
                    'FLOATNUM' : 'FLOATNUM',
                    'number_binary_operation' : 'unknown',
                    'unknown' : 'unknown',
                  }),
                'number_binary_operation' : defaultdict(lambda : 'error_op_not_sup',
                  {
                    'INTNUM' : 'INTNUM',
                    'FLOATNUM' : 'FLOATNUM',
                    'number_binary_operation' : 'unknown',
                    'unknown' : 'unknown',
                  }),
                # Arrays
                'array' :                   'error_op_not_sup',
                'TRANSPOSE':                'error_op_not_sup',
                'unary_minus' :             'error_op_not_sup',
                'matrix_binary_operation' : 'error_op_not_sup',
                # String
                'STRING' :                  'error_op_not_sup',
              })
          })

        # Operation assignment
        cls.TYPE_MAP['-='] = op_assign_map
        cls.TYPE_MAP['*='] = op_assign_map
        cls.TYPE_MAP['/='] = op_assign_map
        cls.TYPE_MAP['+='] = op_assign_map.copy()

        cls.TYPE_MAP['+=']['ID'] = op_assign_id_map.copy()
        cls.TYPE_MAP['+=']['ID']['STRING'] = defaultdict(lambda : 'error_op_not_sup',
          {
            'STRING' : 'ASSIGN',
          })

        bool_exp_map = defaultdict(lambda : 'error_op_not_sup',
          {
            'unknown' :                   'boolean_expression',
            'number_binary_expression' :  'boolean_expression',
            'INTNUM' :                    'boolean_expression',
            'FLOATNUM' :                  'boolean_expression',
          })

        cls.TYPE_MAP['bool'] = defaultdict(lambda : 'error_op_not_sup',
          {
            'unknown' : bool_exp_map,
            'number_binary_expression' : bool_exp_map,
            'INTNUM' : bool_exp_map,
            'FLOATNUM': bool_exp_map,
            'STRING' : defaultdict(lambda : 'error_op_not_sup',
              {
                'STRING' : 'boolean_expression'
              }),

          })

    def visit_Program(self, node):
        self.symbol_table = SymbolTable('program', 'program_table')
        self.loop_scopes_cnt = 0
        if node.instructions_opt:
            self.visit(node.instructions_opt)
        return node.type

    def variable_declared(self, node):
        if self.symbol_table.get(node.name) is None:
            print((f'ERROR in line {node.lineno}\n'
                   f'{node.name} is not declared\n'))
            self.GOT_ERROR = True
            return False
        return True

    def visit_Block(self, node):
        self.visit(node.instructions)
        node.in_type = node.type
        return node.in_type

    def visit_Assignment(self, node):
        right = node.right
        left = node.left
        type_left = left.type
        type_right = self.visit(right)

        if type_right == 'ID':
            if self.variable_declared(right):
                right = self.symbol_table.get(right.name)
                type_right = self.visit(right)

        num_rows = -1
        num_cols = -1
        elem_type_left = type_left
        # Get more precise left type. There are only two options
        # available for type_left: ID and array_element (it is due
        # to parser's specification)
        if type_left == 'ID' and node.operator != '=':
            if self.variable_declared(left):
                left = self.symbol_table.get(left.name)
                type_left = self.visit(left)
                elem_type_left = type_left
        elif type_left == 'array_element':
            if isinstance(left.array, ast.String):
                print((f'ERROR in line {node.lineno}\n'
                       f'Assignment to entity not being variable\n'))
                self.GOT_ERROR = True
                return node.type
            self.visit(left)
            if left.array.type == 'STRING':
                left = left.array
                type_left = 'STRING'
                if node.operator != '=':
                    print((f'ERROR in line {node.lineno}\n'
                           f'Operational assignment to a substring\n'))
                    self.GOT_ERROR = True
                    return node.type
            else:
                left = self.symbol_table.get(left.array.name)
                type_left = self.visit(left)
                elem_type_left = type_left
                if type_left != 'STRING':
                    elem_type_left = left.element_type
                    num_rows = node.left.num_rows
                    num_cols = node.left.num_cols
                    if num_rows == 1 and num_cols == 1:
                        if left.element_type not in ['INTNUM', 'FLOATNUM', 'unknown']:
                            type_left = left.list.elements[0].element_type
                        else:
                            type_left = elem_type_left

        result_type = self.get_type(node.operator, node.left.type,
                                    type_right, type_left)

        if result_type == 'error_left_invalid':
            print((f'ERROR in line {node.lineno}\n'
                   f'Cannot assign to {left.type}\n'))
            self.GOT_ERROR = True
            return node.type

        if result_type == 'error_right_invalid':
            print((f'ERROR in line {node.lineno}\n'
                   f'{type_right} is not a valid type '
                   f'for the right side of assignment\n'))
            self.GOT_ERROR = True
            return node.type

        if result_type == 'error_op_not_sup':
            print((f'ERROR in line {node.lineno}\n'
                   f'Cannot {node.operator} assign type {type_right} '
                   f'to array of type {elem_type_left}\n'))
            self.GOT_ERROR = True
            return node.type

        if node.operator == '=':
            if result_type == 'array':
                if (right.num_rows != 'unknown' and right.num_cols != 'unknown' and
                        num_rows != 'unknown' and num_cols != 'unknown' and
                        (right.num_rows != num_rows or right.num_cols != num_cols)):
                    print((f'ERROR in line {node.lineno}\n'
                           f'Inconsistent dimensions of arrays\n'))
                    node.left.array.element_type = 'unknown'
                    self.GOT_ERROR = True
                    return node.type

            # result_type can be FLOATNUM or INTNUM only when we assign
            # to a subarray or array element. This is how we infer
            # the type of resulting array element.
            if result_type in ['unknown', 'FLOATNUM', 'INTNUM']:
                node.left.array.element_type = result_type
        else:
            if result_type in ['unknown', 'FLOATNUM', 'INTNUM']:
                node.left.array.element_type = result_type

        # Add symbol to symbol table.
        if node.left.type != 'array_element':
            self.symbol_table.put(node.left.name, node.right)

        return node.type

    def visit_For(self, node):
        self.visit(node.variable)
        self.visit(node.range)
        self.symbol_table.push_scope('loop')
        self.loop_scopes_cnt += 1
        if self.symbol_table.get(node.variable.name) is not None:
            print((f'ERROR in line {node.lineno}\n'
                   f'{node.variable.name} cannot be an iterating variable, '
                   'it was already declared\n'))
            self.GOT_ERROR = True
        else:
            self.symbol_table.put(node.variable.name, ast.IntNum(node.range.start_value.value))
        self.visit(node.instruction)
        self.loop_scopes_cnt -= 1
        self.symbol_table.pop_scope()
        return node.type

    def visit_While(self, node):
        self.visit(node.condition)
        self.symbol_table.push_scope('loop')
        self.loop_scopes_cnt += 1
        self.visit(node.instruction)
        self.loop_scopes_cnt -= 1
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

        return node.type

    def visit_Break(self, node):
        if self.loop_scopes_cnt == 0:
            print((f'ERROR in line {node.lineno}\n'
                   f'Cannot break from current scope\n'))
            self.GOT_ERROR = True

        return node.type

    def visit_Continue(self, node):
        if self.loop_scopes_cnt == 0:
            print((f'ERROR in line {node.lineno}\n'
                   f'Cannot continue in current scope\n'))
            self.GOT_ERROR = True

        return node.type

    def visit_Return(self, node):
        if node.args is not None:
            self.visit(node.args)
        return node.type

    def visit_Print(self, node):
        self.visit(node.args)
        return node.type

    def visit_ArrayElement(self, node):
        self.visit(node.array)
        self.visit(node.ids)

        if node.array.type == 'STRING':
            # Check correcntess of indexes
            indices = node.ids.elements
            if len(indices) > 2 or (len(indices) == 2 and indices[0].value != 0):
                print((f'ERROR in line {node.lineno}\n'
                       f'Indices inconsistent with dimensions \n'))
                self.GOT_ERROR = True
                return node.type
            return 'STRING'
        else:
            self.variable_declared(node.array)
            array = self.symbol_table.get(node.array.name)
            type_array = self.visit(array)
            if type_array == 'STRING':
                indices = node.ids.elements
                if len(indices) > 2 or (len(indices) == 2 and indices[0].value != 0):
                    print((f'ERROR in line {node.lineno}\n'
                           f'Indices inconsistent with dimensions \n'))
                    self.GOT_ERROR = True
                return 'STRING'
            elif type_array in ['array', 'matrix_binary_operation']:
                num_rows = array.num_rows
                num_cols = array.num_cols
            elif type_array == 'unknown':
                return node.type
            else:
                print((f'ERROR in line {node.lineno}\n'
                       f'Subscripted value is neither array nor string\n'))
                self.GOT_ERROR = True
                return node.type

        indices_num = len(node.ids.elements)
        new_row_num = 1
        new_col_num = 1
        if indices_num > 2:
            print((f'ERROR in line {node.lineno}\n'
                   f'Indices inconsistent with dimensions \n'))
            self.GOT_ERROR = True
            return node.type
        elif len(node.ids.elements) == 2:
            row_idx = node.ids.elements[0]
            col_idx = node.ids.elements[1]
            if row_idx.type == 'range':
                if num_rows != 'unknown' and row_idx.end_value.value > num_rows:
                    print((f'ERROR in line {node.lineno}\n'
                           f'Row index out of range\n'))
                    self.GOT_ERROR = True
                new_row_num = row_idx.end_value.value - row_idx.start_value.value
            elif row_idx.type == 'INTNUM':
                if num_rows != 'unknown' and row_idx.value >= num_rows:
                    print((f'ERROR in line {node.lineno}\n'
                           f'Row index out of range\n'))
                    self.GOT_ERROR = True
            if col_idx.type == 'range':
                if num_cols != 'unknown' and col_idx.end_value.value > num_cols:
                    print((f'ERROR in line {node.lineno}\n'
                           f'Column index out of range\n'))
                    self.GOT_ERROR = True
                new_col_num = col_idx.end_value.value - col_idx.start_value.value
            elif col_idx.type == 'INTNUM':
                if num_cols != 'unknown' and col_idx.value >= num_cols:
                    print((f'ERROR in line {node.lineno}\n'
                           f'Column index out of range\n'))
                    self.GOT_ERROR = True
            if new_row_num <= 0 or new_col_num <= 0:
                print((f'ERROR in line {node.lineno}\n'
                       f'Wrong indexing\n'))
                self.GOT_ERROR = True
        else:
            row_idx = node.ids.elements[0]
            if num_rows > 1:
                new_col_num = num_cols
            else:
                new_col_num = 1
            if row_idx.type == 'range':
                if num_rows != 'unknown' and row_idx.end_value.value > num_rows:
                    print((f'ERROR in line {node.lineno}\n'
                           f'Index out of range\n'))
                    self.GOT_ERROR = True
                new_row_num = row_idx.end_value.value - row_idx.start_value.value
            elif row_idx.type == 'INTNUM':
                if num_rows != 'unknown' and row_idx.value >= num_rows:
                    print((f'ERROR in line {node.lineno}\n'
                           f'Column index out of range\n'))
                    self.GOT_ERROR = True
            if new_row_num <= 0:
                print((f'ERROR in line {node.lineno}\n'
                       f'Wrong indexing\n'))
                self.GOT_ERROR = True

        node.num_rows = new_row_num
        node.num_cols = new_col_num
        if new_row_num == 1 and new_col_num == 1:
            array = self.symbol_table.get(node.array.name)
            node.element_type = 'unknown'
            if array is not None:
                node.element_type = array.element_type
                return array.element_type
        else:
            node.element_type = array.element_type
            return 'array'

        return node.type

    # Expressions
    @staticmethod
    def visit_IntNum(node):
        return node.type

    @staticmethod
    def visit_FloatNum(node):
        return node.type

    @staticmethod
    def visit_String(node):
        return node.type

    def visit_Array(self, node):
        if node.list is not None:
            self.visit(node.list)
            node.num_rows = node.list.num_rows
            node.num_cols = node.list.num_cols
            if node.list.element_type == 'unary_minus':
                node.element_type = 'unknown'
            else:
                node.element_type = node.list.element_type
        else:
            node.num_rows = 'unknown'
            node.num_cols = 'unknown'
            node.element_type = 'unknown'
        return node.type

    def visit_NumberBinaryOperation(self, node):
        expr_left = node.left
        expr_right = node.right

        type_left = self.visit(expr_left)
        type_right = self.visit(expr_right)

        # Read types of IDs
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

        # Get type of result
        result_type = self.get_type(node.operator, type_left, type_right)

        if result_type == 'error_op_not_sup':
            if type_left == 'matrix_binary_operation':
                type_left = 'array'
            if type_right == 'matrix_binary_operation':
                type_right = 'array'
            print((f'ERROR in line {node.lineno}\n'
                   f'Operation {node.operator} not supported between {type_left} '
                   f'and {type_right}\n'))
            self.GOT_ERROR = True
            return 'number_binary_operation'

        # Check correctness of dimensions for array
        if result_type == 'array':
            # This line deletes preceding dot in elementwise operations
            operator = node.operator[-1]
            element_left_type = expr_left.element_type
            element_right_type = expr_right.element_type
            if element_left_type in ['array', 'TRANSPOSE', 'unary_minus', 'matrix_bin_op']:
                element_left_type = expr_left.list.elements[0].element_type
            if element_right_type in ['array', 'TRANSPOSE', 'unary_minus', 'matrix_bin_op']:
                element_right_type = expr_right.list.elements[0].element_type
            node.element_type = self.get_type(operator, element_left_type,
                                              element_right_type)

            if (expr_left.num_cols != 'unknown' and
                    expr_right.num_rows != 'unknown' and
                    expr_left.num_cols != expr_right.num_rows):
                print((f'ERROR in line {node.lineno}\n'
                       f'Inconsistent shape. Cannot {node.operator} '
                       f'matrices of shape {expr_left.num_rows}x{expr_left.num_cols} '
                       f'and {expr_right.num_rows}x{expr_right.num_cols}\n'))
                self.GOT_ERROR = True
                node.num_rows = expr_left.num_rows
                node.num_cols = expr_right.num_cols
                return 'matrix_binary_operation'
            else:
                node.num_rows = expr_left.num_rows
                node.num_cols = expr_right.num_cols
                return result_type

        return result_type

    def visit_MatrixBinaryOperation(self, node):
        """If successful will return 'array' type if not successful will return
    'matrix_binary_operation'. Either way, the node will have num_rows, num_cols
    attributes, which may be set to unknown.
    """

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

        result_type = self.get_type(node.operator, type_left, type_right)

        if type_left == 'unknown' or type_right == 'unknown':
            node.num_rows = 'unknown'
            node.num_cols = 'unknown'
            node.element_type = 'unknown'
            return result_type

        if result_type == 'array':
            if expr_left.element_type == 'unknown' or expr_right.element_type == 'unknown':
                node.element_type = 'unknown'
            else:
                element_left_type = expr_left.element_type
                element_right_type = expr_right.element_type
                if element_left_type in ['array', 'TRANSPOSE', 'unary_minus', 'matrix_bin_op']:
                    element_left_type = expr_left.list.elements[0].element_type
                if element_right_type in ['array', 'TRANSPOSE', 'unary_minus', 'matrix_bin_op']:
                    element_right_type = expr_right.list.elements[0].element_type
                element_type = self.get_type(node.operator[1], element_left_type, element_right_type)
                if element_type == 'error_op_not_sup':
                    print((f'ERROR in line {node.lineno}\n'
                           f'Operation {node.operator} not supported between array of {type_left} '
                           f'and array of {type_right}\n'))
                    self.GOT_ERROR = True
                    return 'matrix_binary_operation'

            if expr_left.num_rows == 'unknown' or expr_right.num_rows == 'unknown':
                num_rows = 'unknown'
            else:
                num_rows = expr_left.num_rows

            if expr_left.num_cols == 'unknown' or expr_right.num_cols == 'unknown':
                num_cols = 'unknown'
            else:
                num_cols = expr_left.num_cols

            # Matrix dimensions correctness check
            if ((num_cols != 'unknown' and expr_right.num_cols != expr_left.num_cols) or
                    (num_rows != 'unknown' and expr_right.num_rows != expr_left.num_rows)):
                print((f'ERROR in line {node.lineno}\n'
                       f'Inconsistent shape. Cannot {node.operator} '
                       f'matrices of shape {expr_left.num_rows}x{expr_left.num_cols} '
                       f'and {expr_right.num_rows}x{expr_right.num_cols}\n'))
                self.GOT_ERROR = True
                node.num_rows = 'unknown'
                node.num_cols = 'unknown'
                node.element_type = 'unknown'
                return node.type
            else:
                node.num_rows = num_rows
                node.num_cols = num_cols
                element_left_type = expr_left.element_type
                if element_left_type in ['array', 'TRANSPOSE', 'unary_minus', 'matrix_bin_op']:
                    element_left_type = expr_left.list.elements[0].element_type
                node.element_type = element_left_type
                return result_type

        print((f'ERROR in line {node.lineno}\n'
               f'Operation {node.operator} not supported between {type_left} '
               f'and {type_right}\n'))
        self.GOT_ERROR = True

        node.num_rows = 'unknown'
        node.num_cols = 'unknown'
        return result_type

    def visit_BooleanExpression(self, node):
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

        result_type = self.get_type('bool', type_left, type_right)

        if result_type == 'error_op_not_sup':
            print((f'ERROR in line {node.lineno}\n'
                   f'Operator {node.operator} not supported between {type_left} '
                   f'and {type_right}\n'))
            self.GOT_ERROR = True

        return node.type

    def visit_MatrixFunction(self, node):
        parameters = node.parameter
        self.visit(parameters)
        if parameters.num_rows != 1 and parameters.num_cols > 2:
            print((f'ERROR in line {node.lineno}\n'
                   f'{parameters} are not valid matrix function arguments\n'))
            self.GOT_ERROR = True
        parameter = parameters.elements[0]
        parameter_type = self.visit(parameter)
        if parameter_type == 'ID':
            if self.variable_declared(parameter):
                parameter = self.symbol_table.get(parameter.name)
                parameter_type = self.visit(parameter)
            else:
                node.num_rows = 'unknown'
        if parameter_type == 'INTNUM':
            if hasattr(parameter, 'value'):
                node.num_rows = parameter.value
            else:
                node.num_rows = 'unknown'
        else:
            print((f'ERROR in line {node.lineno}\n'
                   f'Matrix function {node.function} cannot take '
                   f'{parameter} as parameter\n'))
            self.GOT_ERROR = True
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
                self.GOT_ERROR = True
                node.num_cols = 'unknown'
        else:
            node.num_cols = node.num_rows

        node.element_type = 'INTNUM'

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
            self.GOT_ERROR = True
        elif value_type == 'array':
            node.num_cols = value.num_cols
            node.num_rows = value.num_rows

        return value_type

    def visit_Transpose(self, node):
        value = node.value
        value_type = self.visit(value)
        node.element_type = value.element_type if hasattr(value, 'element_type') else 'unknown'
        if value_type == 'ID':
            if not self.variable_declared(value):
                value_type = 'unknown'
            else:
                value = self.symbol_table.get(value.name)
                value_type = self.visit(value)

        if value_type in ['array', 'TRANSPOSE', 'matrix_binary_operation']:
            node.num_cols = value.num_rows
            node.num_rows = value.num_cols
        else:
            print((f'ERROR in line {node.lineno}\n'
                   f'Cannot transpose {value_type}\n'))
            self.GOT_ERROR = True
            value_type = 'TRANSPOSE'
            node.num_cols = 'unknown'
            node.num_rows = 'unknown'

        return value_type

    # Other
    @staticmethod
    def visit_Identifier(node):
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

        if end_type == 'ID':
            if not self.variable_declared(end_value):
                end_type = 'unknown'
            else:
                end_value = self.symbol_table.get(end_value.name)
                end_type = self.visit(end_value)

        if start_type not in ['INTNUM', 'array_element', 'unknown']:
            print((f'ERROR in line {node.lineno}\n'
                   f'{start_type} is not a valid type for a range start\n'))
            self.GOT_ERROR = True

        if end_type not in ['INTNUM', 'array_element', 'unknown']:
            print((f'ERROR in line {node.lineno}\n'
                   f'{end_type} is not a valid type for a range start\n'))
            self.GOT_ERROR = True

        return node.type

    def visit_InnerList(self, node):
        first_elem = node.elements[0]
        first_elem_type = self.visit(first_elem)
        node.num_rows = 'unknown'
        node.num_cols = 'unknown'
        node.element_type = 'unknown'
        if (first_elem_type == 'array' and
                first_elem.type not in ['matrix_function', 'TRANSPOSE'] and
                first_elem.list is not None and
                first_elem.list.elements[0].type == 'array'):
            print((f'ERROR in line {node.lineno}\n'
                   'Matrix can have maximum 2 dimensions\n'))
            self.GOT_ERROR = True
            return node.type
        for elem in node.elements[1:]:
            elem_type = self.visit(elem)
            if elem_type != first_elem_type:
                print((f'ERROR in line {node.lineno}\n'
                       f'Inconsistent types {first_elem_type} and {elem_type} in the array\n'))
                self.GOT_ERROR = True
                return node.type
            elif first_elem_type == 'array' and first_elem.num_cols != elem.num_cols:
                print((f'ERROR in line {node.lineno}\n'
                       f'Inconsistent shapes {first_elem.num_cols} and {elem.num_cols} in the array\n'))
                self.GOT_ERROR = True
                return node.type

        node.element_type = first_elem_type

        if node.element_type == 'array':
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

            if elem_type not in ['INTNUM', 'range', 'unknown']:
                print((f'ERROR in line {node.lineno}\n'
                       f'{elem_type} is not a valid array index type\n'))
                self.GOT_ERROR = True
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
