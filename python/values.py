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
            'add': BuiltinFunction(lambda v: self.add(v)),
            'sub': BuiltinFunction(lambda v: self.sub(v)),
            'mul': BuiltinFunction(lambda v: self.mul(v)),
            'div': BuiltinFunction(lambda v: self.div(v)),
            'pow': BuiltinFunction(lambda v: self.power(v)),
            'npow': BuiltinFunction(lambda v: self.neg_power(v))
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