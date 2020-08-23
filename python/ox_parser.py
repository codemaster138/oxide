from pos import Position as Pos
from utils import NodeList

##################################
#             PARSER             #
##################################
# This file contains all parser logic

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
    
    def failure(self, error):
        self.error = error
        return self
    
    def success(self, node):
        #print('Succeded with', node)
        self.node = node
        return self
    
    def register(self, res):
        #print(f"\x1b[32mpassed" + ('\x1b[31;1m' if res == None else ''), res, "\x1b[0m")
        if res.error:
            self.error = res.error
            return self
        return res.node

class Parser:
    def __init__(self, tokens, generator):
        self.tokens = tokens
        self.cur_token = None
        self.tok_idx = -1
        self.advance()
        self.generator = generator
    
    # Advance by 1 token in the list
    def advance(self):
        # Increment index
        self.tok_idx += 1
        # Check if there are any more tokens
        if self.tok_idx < len(self.tokens):
            # Set the current token
            self.cur_token = self.tokens[self.tok_idx]
        else:
            # Otherwise, unset cur_token
            self.cur_token = None

    # Generate an AST (= Abstract Syntax Tree)
    def gen_ast(self) -> NodeList:
        res = ParseResult()
        node = res.register(self.generator(self))
        if res.error: return res
        return res.success(node)