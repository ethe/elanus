# -*- coding: utf-8 -*-
from utils.singleton import Singleton


class Node(object):
    def __init__(self, line=0):
        self.line = line


class Expressions(Node):
    def __init__(self, expressions, line=0):
        super(Expressions, self).__init__(line)
        self.expressions = expressions

    def __eq__(self, another):
        if not isinstance(another, Expressions):
            return False
        return self.expressions == another.expressions

    def __getitem__(self, key):
        return self.expressions.__getitem__(key)

    def __repr__(self):
        return "<Expressions {}>".format(self.expressions)


class Expression(Node):
    def __repr__(self):
        return "<{} {}>".format(self.__class__, self.value if hasattr(self, "value") else self.__hash__())


class Function(Expression):
    def __init__(self, name=None, args=[], expressions=Expressions([]), line=0):
        self.name = name
        self.args = args
        self.expressions = expressions

    def __eq__(self, another):
        if not isinstance(another, Function):
            return False
        return self.name == another.name and self.args == another.args and self.expressions == another.expressions

    def __repr__(self):
        return "<Function {}>".format(self.name)


class Call(Expression):
    def __init__(self, name="", args=[], line=0):
        super(Call, self).__init__(line)
        self.name = name
        self.args = args

    def __eq__(self, another):
        if not isinstance(another, Call):
            return False
        return self.name == another.name and self.args == another.args

    def __repr__(self):
        return "<Call {} {}>".format(self.name, self.args)


class Bind(Expression):
    def __init__(self, name, value, line=0):
        super(Expression, self).__init__(line)
        self.name = name
        self.value = value

    def __eq__(self, another):
        if not isinstance(another, Bind):
            return False
        return self.name == another.name and self.value == another.value

    def __repr__(self):
        return "<Bind {} {}>".format(self.name, self.value)


class Unit(Expression):
    def __init__(self, call=None, line=0):
        super(Expression, self).__init__(line)
        self.call = call

    def __eq__(self, another):
        if not isinstance(another, Unit):
            return False
        return self.call == another.call

    def __repr__(self):
        return "<Unit {}>".format(self.call)


class Number(Expression):
    def __init__(self, number, line=0):
        super(Number, self).__init__(line)
        self.value = number

    def __eq__(self, another):
        if not isinstance(another, Number):
            return False
        return self.value == another.value

    def __repr__(self):
        return str(self.value)


class Int(Number):
    def __init__(self, number, line=0):
        super(Int, self).__init__(int(number), line)


class Float(Number):
    def __init__(self, number, line=0):
        super(Float, self).__init__(float(number), line)


class Return(Expression):
    def __init__(self, expression, line=0):
        self.expression = expression
        self.line = line

    def __repr__(self):
        return "<Return {}>".format(self.expression)

    def __eq__(self, another):
        if isinstance(another, Return):
            return self.expression == self.expression
        return False


class Void(Expression):
    def __init__(self, line=0):
        self.line = line

    def __repr__(self):
        return "<Void void>"

    def __eq__(self, another):
        if isinstance(another, Void):
            return True
        return False


class Nil(Singleton, Expression):
    def __init__(self, line=0):
        self.line = line

    def __repr__(self):
        return 'nil'

    def __eq__(self, another):
        return self is another


class Bool(Singleton, Expression):
    def __init__(self, line=0):
        self.line = line

    def __eq__(self, another):
        return self is another


class TrueType(Bool):
    def __init__(self, line=0):
        super(TrueType, self).__init__(line=line)
        self.value = True

    def __repr__(self):
        return "true"


class FalseType(Bool):
    def __init__(self, line=0):
        super(FalseType, self).__init__(line=line)
        self.value = False

    def __repr__(self):
        return "false"


class Closure(object):
    def __init__(self, function, environment):
        self.function = function
        self.environment = environment

    def __repr__(self):
        return "<Closure {}>".format(self.function.name)


class BuiltinFunction(Function):
    def __init__(self, name=None, args=[], expressions=Expressions([]), line=0):
        super(BuiltinFunction, self).__init__(name=name, args=args, expressions=expressions, line=line)

    def call(self, interpret, environment):
        self.values = []
        for i in self.args:
            self.values.append(interpret(environment[i], environment).value)
        return self.oprate()
