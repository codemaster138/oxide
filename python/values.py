from abc import ABCMeta, abstractmethod

class Value(metaclass=ABCMeta):
    def __init__(self):
        self.functions = {}
    
    @abstractmethod
    def before(self, value):
        pass

    @abstractmethod
    def operation(self, op, *args):
        pass

class FunctionValue(Value, metaclass=ABCMeta):
    @abstractmethod
    def execute(self, *args):
        pass

    def before(self, value):
        pass

    def operation(self, op, *args):
        pass

class BuiltinFunction(FunctionValue):
    def __init__(self, code):
        self.code = code

    def execute(self, *args):
        return self.code(*args)

class Number(Value):
    def __init__(self, value):
        self.value = float(value)
        self.set_functions()
    
    def set_functions(self):
        self.functions = {
            '__add__': BuiltinFunction(lambda v: self.add(v)),
            '__sub__': BuiltinFunction(lambda v: self.sub(v)),
            '__mul__': BuiltinFunction(lambda v: self.mul(v)),
            '__div__': BuiltinFunction(lambda v: self.div(v)),
            '__pow__': BuiltinFunction(lambda v: self.power(v)),
            '__npow__': BuiltinFunction(lambda v: self.neg_power(v)),
            '__eq__': BuiltinFunction(lambda v: self.iseq(v)),
            '__neq__': BuiltinFunction(lambda v: self.noteq(v)),
            '__lt__': BuiltinFunction(lambda v: self.less(v)),
            '__gt__': BuiltinFunction(lambda v: self.greater(v))
        }

    @staticmethod
    def before(value):
        try:
            float(value)
            return float(value)
        except:
            return False

    def operation(self, op, *args):
        if self.functions.get(op):
            res = self.functions[op].execute(*args)
            if isinstance(res, str):
                return [None, res]
            return res
        return [None, 'Invalid operation']

    def add(self, v):
        val = self.compat(v)
        if val:
            return [type(self)(self.value + val),None]
        return 'Incompatible Type'

    def sub(self, v):
        val = self.compat(v)
        if val:
            return [type(self)(self.value - val),None]
        return 'Incompatible Type'

    def mul(self, v):
        val = self.compat(v)
        if val:
            return [type(self)(self.value * val),None]
        return 'Incompatible Type'

    def div(self, v):
        val = self.compat(v)
        if val:
            return [type(self)(self.value / val),None]
        return 'Incompatible Type'

    def power(self, v):
        val = self.compat(v)
        if val:
            return [type(self)(self.value ** val),None]
        return 'Incompatible Type'
    
    def neg_power(self, v):
        val = self.compat(v)
        if val:
            return [type(self)(self.value ** (-val)),None]
        return 'Incompatible Type'
    
    def iseq(self, v):
        val = self.compat(v)
        if val:
            return [Boolean("true" if self.value == val else "false"),None]
        return 'Incompatible Type'

    def noteq(self, v):
        val = self.compat(v)
        if val:
            return [Boolean("true" if self.value != val else "false"),None]
        return 'Incompatible Type'

    def less(self, v):
        val = self.compat(v)
        if val:
            return [Boolean("true" if self.value < val else "false"),None]
        return 'Incompatible Type'

    def greater(self, v):
        val = self.compat(v)
        if val:
            return [Boolean("true" if self.value > val else "false"),None]
        return 'Incompatible Type'

    def compat(self, v):
        if isinstance(v, (Number, Boolean)):
            return v.value
        return False
    
    def __repr__(self):
        return str(self.value)

class Boolean(Number):
    def __init__(self, value):
        self.value = 0 if value in (0, "0", "false") else 1
        self.set_functions()
    
    def compat(self, v):
        if isinstance(v, (Number, Boolean)):
            return v.value
        return False
    
    @staticmethod
    def before(value):
        try:
            float(value)
            return float(value)
        except:
            return value if value in ('true', 'false') else False
    
    def __repr__(self):
        return 'true' if self.value else 'false'