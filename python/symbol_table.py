######################################
#            SYMBOL TABLE            #
######################################
from errors import *

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.constants = {}
        self.parent = parent
    
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None:
            value = self.constants.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value
    
    def symbol_exists(self, name):
        ex = name in self.symbols
        if not ex:
            ex = name in self.constants
        if not ex:
            if self.parent != None:
                ex = self.parent.symbol_exists(name)
        return ex
    
    def set(self, name, value, const=False):
        if self.parent:
            if self.parent.symbol_exists(name):
                return self.parent.set(name, value, const)
        if const or name in self.constants:
            if self.symbol_exists(name):
                return "Symbol is a contant"
            self.constants[name] = value
        else:
            self.symbols[name] = value
        return None
    
    def remove(self, name):
        del self.symbols[name]
