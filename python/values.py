from abc import ABCMeta, abstractmethod

class Value(metaclass=ABCMeta):
    def __init__(self):
        self.functions = {}
    
    @abstractmethod
    def before(self, value):
        pass

    def operation(self, op, *args):
        if self.functions.get(op):
            try:
                res = self.functions[op].execute(*args)
            except TypeError as err:
                print(err)
                return [None, 'Missing positional arguments. Maybe invalid Unary Operation?']
            if isinstance(res, str):
                return [None, res]
            return res
        return [None, 'Invalid operation']

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
            '__add__': BuiltinFunction(lambda v=None: self.add(v)),
            '__sub__': BuiltinFunction(lambda v=None: self.sub(v)),
            '__mul__': BuiltinFunction(lambda v: self.mul(v)),
            '__div__': BuiltinFunction(lambda v: self.div(v)),
            '__pow__': BuiltinFunction(lambda v: self.power(v)),
            '__npow__': BuiltinFunction(lambda v: self.neg_power(v)),
            '__eq__': BuiltinFunction(lambda v: self.iseq(v)),
            '__neq__': BuiltinFunction(lambda v: self.noteq(v)),
            '__lt__': BuiltinFunction(lambda v: self.less(v)),
            '__gt__': BuiltinFunction(lambda v: self.greater(v)),
            '__lte__': BuiltinFunction(lambda v: self.less_eq(v)),
            '__gte__': BuiltinFunction(lambda v: self.greater_eq(v)),
            '__not__': BuiltinFunction(lambda: self._not_()),
            '__truey__': BuiltinFunction(lambda: self.isTruey())
        }

    @staticmethod
    def before(value):
        try:
            float(value)
            return float(value) or "0"
        except:
            return False
    
    def getCastType(self, value):
        if type(value).__name__ in ("Number", "Boolean"):
            return Number
        return f'Invalid cast ({type(value).__name__})'

    def operation(self, op, *args):
        if self.functions.get(op):
            try:
                res = self.functions[op].execute(*args)
            except TypeError as err:
                print(err)
                return [None, 'Missing positional arguments. Maybe invalid Unary Operation?']
            if isinstance(res, str):
                return [None, res]
            return res
        return [None, 'Invalid operation']
    
    def isTruey(self):
        return ["false", None] if self.value == 0 else ["true", None]

    def add(self, v):
        if v == None:
            return [self, None]
        val = self.compat(v)
        if val != None:
            cast = self.getCastType(v)
            if isinstance(cast, str):
                return [None, cast]
            return [cast(self.value + val),None]
        return 'Incompatible Type'

    def sub(self, v):
        if v == None:
            return [Number(0 - self.value), None]
        val = self.compat(v)
        if val != None:
            cast = self.getCastType(v)
            if isinstance(cast, str):
                return [None, cast]
            return [cast(self.value - val),None]
        return 'Incompatible Type'

    def mul(self, v):
        val = self.compat(v)
        if val != None:
            cast = self.getCastType(v)
            if isinstance(cast, str):
                return [None, cast]
            return [cast(self.value * val),None]
        return 'Incompatible Type'

    def div(self, v):
        val = self.compat(v)
        if val == 0:
            return [None, 'Cannot divide by 0']
        if val != None:
            cast = self.getCastType(v)
            if isinstance(cast, str):
                return [None, cast]
            return [cast(self.value / val),None]
        return 'Incompatible Type'

    def power(self, v):
        val = self.compat(v)
        if val != None:
            cast = self.getCastType(v)
            if isinstance(cast, str):
                return [None, cast]
            return [cast(self.value ** val),None]
        return 'Incompatible Type'
    
    def neg_power(self, v):
        val = self.compat(v)
        if val != None:
            cast = self.getCastType(v)
            if isinstance(cast, str):
                return [None, cast]
            return [cast(self.value ** (-val)),None]
        return 'Incompatible Type'
    
    def iseq(self, v):
        val = self.compat(v)
        if val != None:
            return [Boolean("true" if self.value == val else "false"),None]
        return 'Incompatible Type'

    def noteq(self, v):
        val = self.compat(v)
        if val != None:
            return [Boolean("true" if self.value != val else "false"),None]
        return 'Incompatible Type'

    def less(self, v):
        val = self.compat(v)
        if val != None:
            return [Boolean("true" if self.value < val else "false"),None]
        return 'Incompatible Type'

    def greater(self, v):
        val = self.compat(v)
        if val != None:
            return [Boolean("true" if self.value > val else "false"),None]
        return 'Incompatible Type'

    def less_eq(self, v):
        val = self.compat(v)
        if val != None:
            return [Boolean("true" if self.value <= val else "false"),None]
        return 'Incompatible Type'

    def greater_eq(self, v):
        val = self.compat(v)
        if val != None:
            return [Boolean("true" if self.value >= val else "false"),None]
        return 'Incompatible Type'
    
    def _not_(self):
        return [Boolean("true" if self.value == 0 else "false"), None]

    def compat(self, v):
        if isinstance(v, (Number, Boolean)):
            return v.value
        return None
    
    def __repr__(self):
        return f'\x1b[33m{self.value}\x1b[0m'

class Boolean(Number):
    def __init__(self, value):
        self.value = 0 if value in (0, "0", "false") else 1
        self.set_functions()
    
    def compat(self, v):
        if isinstance(v, (Number, Boolean)):
            return v.value or 0
        return False
    
    @staticmethod
    def before(value):
        try:
            float(value)
            return float(value)
        except:
            return value if value in ('true', 'false') else False
    
    def __repr__(self):
        return '\x1b[32mtrue\x1b[0m' if self.value else '\x1b[31;2mfalse\x1b[0m'

class Array(Value):
    def __init__(self, body=[]):
        self.list = []
        for v in body:
            self.list.append(v)
        self.set_functions()
    
    def set_functions(self):
        self.functions = {
            'push': BuiltinFunction(lambda v: self.push(v))
        }
    
    @staticmethod
    def before(v):
        return True
    
    def compat(self, v):
        return None
    
    def push(self, v):
        self.list.append(v)
        return v
    
    def __repr__(self):
        return f'{self.list}'

class Undefined(Value):
    def __init__(self):
        self.set_functions()
    
    def set_functions(self):
        self.functions = {
            '__truey__': BuiltinFunction(lambda:("false", None))
        }
    
    @staticmethod
    def before(v):
        return True
    
    def compat(self, v):
        return False
    
    def __repr__(self):
        return f'\x1b[2mundefined\x1b[0m'