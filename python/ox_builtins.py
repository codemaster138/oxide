from values import *
from interpreter import RTResult

builtin_print = BuiltinFunction(lambda *args: bin_print(*args))
def bin_print(*args):
    res = RTResult()
    print(*args)
    return res.success(Undefined())

def set_builtins(table):
    table.set('print', builtin_print)