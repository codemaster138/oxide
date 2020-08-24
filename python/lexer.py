from re import *
from errors import InvalidCharError
from pos import Position as Pos 
from token import Token

def set_keywords(*args):
    keyword_re = r"(?:" + "|".join(args) + r")"
    return keyword_re

lexems = {
    # Separators
    'SEMICOLON': r";",
    'COMMA': r",",
    # Comparison operators
    'EE': r"==",
    'GT': r">",
    'LT': r"<",
    'GTE': r">=",
    'LTE': r"<=",
    'NE': r'!=',
    'NOT': r"!",
    'AND': r'&&',
    'OR': r'\|\|',
    # Assignment operators
    'EQ': r"=",
    # Numbers
    'FLOAT': r"[0-9]+\.[0-9]+",
    'INT': r"[0-9]+",
    # Mathematical operators
    'PLUS': r"\+",
    'MINUS': r"\-",
    'POW': r"\*\*",
    'NPOW': r"\/\/",
    'MUL': r"\*",
    'DIV': r"\/",
    # Precedence
    'LPAREN': r"\(",
    'RPAREN': r"\)",
    'LCURL': r"{",
    'RCURL': r"}",
    'LBRACK': r"\[",
    'RBRACK': r"]",
    # Booleans
    'FALSE': r"false",
    'TRUE': r"true",
    # Misc
    'UNDEF': r"undefined",
    'KEYWORD': set_keywords('if','else', 'var'),
    'IDENTIFIER': r"\w+"
}

class Lexer:
    def __init__(self, fn:str, text:str, skip:str, lexems:dict) -> None:
        self.text = text
        self.selection = None
        self.position = Pos(fn, text)
        self.advance()
        self.lexems = lexems
        self.skip = skip

    def advance(self, t=""):
        self.position.advance(t)
        if self.position.idx > len(self.text):
            self.selection = None
            return
        self.selection = self.text[self.position.idx:]

    def make_tokens(self):
        tokens = []

        while self.selection != "":
            match = None
            tp = None
            pos_start = self.position.copy()
            if self.selection[0] in self.skip:
                self.advance(self.selection[0])
                continue
            for k, v in self.lexems.items():
                res = search(v, self.selection)
                if res != None and res.span()[0] == 0:
                    tp = k
                    match = res.group()
                    break
            if not match:
                return [None, InvalidCharError(self.selection[0], self.position)]
            else:
                self.advance(match)
                tokens.append(Token(tp, match, pos_start, self.position.copy()))
        tokens.append(Token('EOF', 'EOF', self.position.copy(), self.position.copy()))
        return [tokens, None]

def generate(fn, text):
    return Lexer(fn, text, "  \t", lexems).make_tokens()