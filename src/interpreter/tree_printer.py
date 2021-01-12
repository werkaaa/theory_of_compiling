from interpreter.ast import *


# noinspection PyPep8Naming
def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def print_intended(to_print, intend):
    print(intend * "|  " + to_print)


# noinspection PyPep8Naming,PyUnresolvedReferences
class TreePrinter:

    # General
    @addToClass(Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(Instruction)
    def printTree(self, indent=0):
        print_intended(self.type, indent)

    @addToClass(Expression)
    def printTree(self, indent=0):
        print_intended(self.type, indent)

    # Instructions
    @addToClass(Block)
    def printTree(self, indent=0):
        print_intended(self.type, indent)
        if self.instructions is not None:
            self.instructions.printTree(indent + 1)

    @addToClass(Assignment)
    def printTree(self, indent=0):
        print_intended(self.operator, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(For)
    def printTree(self, indent=0):
        print_intended(self.type, indent)
        self.variable.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(While)
    def printTree(self, indent=0):
        print_intended(self.type, indent)
        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(If)
    def printTree(self, indent=0):
        print_intended(self.type, indent)
        self.condition.printTree(indent + 1)
        print_intended('then', indent)
        self.if_block.printTree(indent + 1)
        if self.else_block is not None:
            print_intended('else', indent)
            self.else_block.printTree(indent + 1)

    @addToClass(Print)
    def printTree(self, indent=0):
        print_intended(self.type, indent)
        self.args.printTree(indent + 1)

    @addToClass(Return)
    def printTree(self, indent=0):
        print_intended(self.type, indent)
        if self.args is not None:
            self.args.printTree(indent + 1)

    @addToClass(ArrayElement)
    def printTree(self, indent=0):
        print_intended("get_element", indent)
        self.array.printTree(indent + 1)
        self.ids.printTree(indent + 1)

    # Expressions
    @addToClass(Value)
    def printTree(self, indent=0):
        print_intended(str(self.value), indent)

    @addToClass(Array)
    def printTree(self, indent=0):
        if self.list is not None:
            print_intended('array', indent)
            self.list.printTree(indent + 1)
        else:
            print_intended('empty_array', indent)

    @addToClass(BinaryExpression)
    def printTree(self, indent=0):
        print_intended(self.operator, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(MatrixFunction)
    def printTree(self, indent=0):
        print_intended(self.function, indent)
        self.parameter.printTree(indent + 1)

    @addToClass(UnaryMinus)
    def printTree(self, indent=0):
        print_intended('-', indent)
        self.value.printTree(indent + 1)

    @addToClass(Transpose)
    def printTree(self, indent=0):
        print_intended(self.type, indent)
        self.value.printTree(indent + 1)

    # Other
    @addToClass(Program)
    def printTree(self, indent=0):
        print_intended(self.type, indent)
        self.instructions_opt.printTree(indent + 1)

    @addToClass(Identifier)
    def printTree(self, indent=0):
        print_intended(self.name, indent)

    @addToClass(Range)
    def printTree(self, indent=0):
        print_intended(self.type, indent)
        self.start_value.printTree(indent + 1)
        self.end_value.printTree(indent + 1)

    @addToClass(List)
    def printTree(self, indent=0):
        for element in self.elements:
            element.printTree(indent)
