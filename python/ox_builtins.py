from values import *
from interpreter import RTResult

builtin_print = BuiltinFunction(lambda *args: bin_print(*args))
def bin_print(*args):
    res = RTResult()
    print(*args)
    return res.success(Undefined())

builtin_input = BuiltinFunction(lambda prompt: bin_input(prompt))
def bin_input(prompt):
    res = RTResult()
    text = input(prompt)
    val = String(text)
    return res.success(val)

def set_builtins(table):
    table.set('print', builtin_print)
    table.set('input', builtin_input)