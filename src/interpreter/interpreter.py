import operator as op
import sys

import numpy as np

from .ast import *
from .exceptions import *
from .memory import *
from .visit import *

sys.setrecursionlimit(10000)


# noinspection PyBroadException
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
            '<': op.lt,
            '>': op.gt,
            '<=': op.le,
            '>=': op.ge,
            '!=': op.ne,
            '==': op.eq,
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

        if len(node.operator) == 2:  # operator of type: +=, -=, *=, /=
            left = self.visit(node.left)
            try:
                right = self.operators[node.operator[0]](left, right)
            except:
                print(f'Runtime error: Invalid types {type(left)} {type(right)} with {node.operator}: line {node.lineno}')
                sys.exit(0)

        if isinstance(node.left, Identifier):
            self.memory_stack.insert(node.left.name, right)
        else:
            self.visit(node.left)
            ids = self.visit(node.left.ids)
            array = self.memory_stack.get(node.left.array.name)

            if isinstance(array, str):
                if len(ids) == 2:
                    if ids[0] != 0:
                        print(f'Runtime error: Wrong indexing: line {node.lineno}')
                        sys.exit(0)
                    else:
                        ids = ids[1]
                if isinstance(ids[0], range):
                    fst_idx = ids[0].start
                    snd_idx = ids[0].stop
                else:
                    fst_idx = ids[0]
                    snd_idx = fst_idx + 1
                try:
                    result = array[:fst_idx] + right + array[snd_idx:]
                except IndexError:
                    print(f'Runtime error: Wrong indexing: line {node.lineno}')
                    sys.exit(0)
                self.memory_stack.insert(node.left.array.name, result)
            else:
                if len(ids) == 2:
                    if isinstance(ids[0], range):
                        fst_idx = slice(ids[0].start, ids[0].stop)
                    else:
                        fst_idx = ids[0]
                    if isinstance(ids[1], range):
                        snd_idx = slice(ids[1].start, ids[1].stop)
                    else:
                        snd_idx = ids[1]
                    try:
                        array[fst_idx, snd_idx] = right
                    except IndexError:
                        print(f'Runtime error: Wrong indexing: line {node.lineno}')
                        sys.exit(0)
                else:
                    try:
                        array[tuple(ids)] = right
                    except IndexError:
                        print(f'Runtime error: Wrong indexing: line {node.lineno}')
                        sys.exit(0)

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
        array = self.visit(node.array)
        ids = self.visit(node.ids)
        if isinstance(array, str):
            if len(ids) == 2:
                ids = ids[1]
            else:
                ids = ids[0]
            if isinstance(ids, range):
                start = int(ids.start) + 1
                end = int(ids.stop) + 1
            else:
                start = ids + 1
                end = start + 1
            try:
                result = array[start:end]
            except IndexError:
                print(f'Runtime error: Wrong indexing: line {node.lineno}')
                sys.exit(0)
            return result
        else:
            if len(ids) == 2:
                if isinstance(ids[0], range):
                    fst_idx = slice(ids[0].start, ids[0].stop)
                else:
                    fst_idx = ids[0]
                if isinstance(ids[1], range):
                    snd_idx = slice(ids[1].start, ids[1].stop)
                else:
                    snd_idx = ids[1]
                try:
                    result = array[fst_idx, snd_idx]
                except IndexError:
                    print(f'Runtime error: Wrong indexing: line {node.lineno}')
                    sys.exit(0)
                return result
            else:
                try:
                    result = array[tuple(ids)]
                except IndexError:
                    print(f'Runtime error: Wrong indexing: line {node.lineno}')
                    sys.exit(0)
                return result

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
        left = self.visit(node.left)
        right = self.visit(node.right)
        return self.operators[node.operator](left, right)

    @when(MatrixFunction)
    def visit(self, node):
        parameter = self.visit(node.parameter)
        num_rows = parameter[0]
        num_cols = parameter[1] if len(parameter) > 1 else None
        if node.function == 'eye':
            return np.eye(num_rows, dtype=int)
        elif node.function == 'ones':
            if num_cols is not None:
                return np.ones((num_rows, num_cols), dtype=int)
            else:
                return np.ones(num_rows, dtype=int)
        elif node.function == 'zeros':
            if num_cols is not None:
                return np.zeros((num_rows, num_cols), dtype=int)
            else:
                return np.zeros(num_rows, dtype=int)

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
