from re import *
from errors import
from pos import Position as Pos 
from token import Token

lexems = {
    'FLOAT': r"[0-9]+\.[0-9]+",
    'INT': r"[0-9]+",
    'PLUS': r"\+",
    'MINUS': r"\-",
    'MUL': r"\*"
    'DIV': r"\/"
}

class Lexer:
    def __init__(self, fn:str, text:str, lexems:dict):
        self.text = text
        self.selection = None
        self.position = Pos(fn)
        self.advance()
        self.lexems = lexems

    def advance(self, t=""):
        self.position.advance(t)
        if self.position.idx > self.text.length:
            self.selection = None
            return
        self.selection = self.text[self.position.idx:]

    def make_tokens():
        tokens = []

        while self.selection:
            match = None
            tp = None
            for k, v in self.lexems.items():
                res = search(v, self.selection)
                if res != None and res.span()[0] == 0:
                    tp = k
                    match = res.group(0)
                    break
            if not match:
                return [None, InvalidCharError(self.selection[0], self.position)]
            else:
                self.position.advance(match)
                tokens.append(Token(tp, match))

        return [tokens, None]