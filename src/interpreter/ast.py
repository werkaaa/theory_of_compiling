class Node:
    def __init__(self):
        self.type = 'Node'


class Instruction(Node):
    pass


class Expression(Node):
    pass


# Instructions
class Block(Instruction):
    def __init__(self, instructions):
        super().__init__()
        self.type = 'INSTRUCTIONS_BLOCK'
        self.instructions = instructions


class Assignment(Instruction):
    def __init__(self, left, operator, right):
        super().__init__()
        self.type = 'ASSIGN'
        self.left = left
        self.operator = operator
        self.right = right


# noinspection PyShadowingBuiltins
class For(Instruction):
    def __init__(self, variable, range, instruction):
        super().__init__()
        self.type = 'FOR'
        self.variable = variable
        self.range = range
        self.instruction = instruction


class While(Instruction):
    def __init__(self, condition, instruction):
        super().__init__()
        self.type = 'WHILE'
        self.condition = condition
        self.instruction = instruction


class If(Instruction):
    def __init__(self, condition, if_block, else_block=None):
        super().__init__()
        self.type = 'IF'
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block


class Break(Instruction):
    def __init__(self):
        super().__init__()
        self.type = 'BREAK'


class Continue(Instruction):
    def __init__(self):
        super().__init__()
        self.type = 'CONTINUE'


class Return(Instruction):
    def __init__(self, args=None):
        super().__init__()
        self.type = 'RETURN'
        self.args = args


class Print(Instruction):
    def __init__(self, args=None):
        super().__init__()
        self.type = 'PRINT'
        self.args = args


class ArrayElement(Expression):
    def __init__(self, array, ids):
        super().__init__()
        self.type = 'array_element'
        self.array = array
        self.ids = ids


# Expressions
class Value(Expression):
    pass


class IntNum(Value):
    def __init__(self, value):
        super().__init__()
        self.type = 'INTNUM'
        self.value = int(value)


class FloatNum(Value):
    def __init__(self, value):
        super().__init__()
        self.type = 'FLOATNUM'
        self.value = float(value)


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.type = 'STRING'
        self.value = value


# noinspection PyShadowingBuiltins
class Array(Expression):
    def __init__(self, list=None):
        super().__init__()
        self.type = 'array'
        self.list = list


class BinaryExpression(Expression):
    def __init__(self, left, operator, right):
        super().__init__()
        self.type = 'binary_expression'
        self.left = left
        self.operator = operator
        self.right = right


class NumberBinaryOperation(BinaryExpression):
    def __init__(self, left, operator, right):
        super(NumberBinaryOperation, self).__init__(left, operator, right)
        self.type = 'number_binary_operation'


class MatrixBinaryOperation(BinaryExpression):
    def __init__(self, left, operator, right):
        super(MatrixBinaryOperation, self).__init__(left, operator, right)
        self.type = 'matrix_binary_operation'


class BooleanExpression(BinaryExpression):
    def __init__(self, left, operator, right):
        super(BooleanExpression, self).__init__(left, operator, right)
        self.type = 'boolean_expression'


class MatrixFunction(Expression):
    def __init__(self, function, parameter):
        super().__init__()
        self.type = 'matrix_function'
        self.function = function
        self.parameter = parameter


class UnaryMinus(Expression):
    def __init__(self, value):
        super().__init__()
        self.type = 'unary_minus'
        self.value = value


class Transpose(Expression):
    def __init__(self, value):
        super().__init__()
        self.type = 'TRANSPOSE'
        self.value = value


# Other
class Program(Node):
    def __init__(self, instructions_opt):
        super().__init__()
        self.type = 'program'
        self.instructions_opt = instructions_opt


class Identifier(Node):
    def __init__(self, name):
        super().__init__()
        self.type = 'ID'
        self.name = name


class Range(Node):
    def __init__(self, start_value, end_value):
        super().__init__()
        self.type = 'range'
        self.start_value = start_value
        self.end_value = end_value


class List(Node):
    def __init__(self, new_element, elements=None):
        super().__init__()
        self.type = 'list'
        self.elements = []
        if elements:
            self.elements = elements.elements

        self.elements.append(new_element)


class InnerList(List):
    def __init__(self, new_element, elements=None):
        super(InnerList, self).__init__(new_element, elements)
        self.type = 'inner_list'


class ListOfIndices(List):
    def __init__(self, new_element, elements=None):
        super(ListOfIndices, self).__init__(new_element, elements)
        self.type = 'list_of_indices'


class ListOfArguments(List):
    def __init__(self, new_element, elements=None):
        super(ListOfArguments, self).__init__(new_element, elements)
        self.type = 'list_of_arguments'


class Instructions(List):
    def __init__(self, new_element, elements=None):
        super(Instructions, self).__init__(new_element, elements)
        self.type = 'instructions'
