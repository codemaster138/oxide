class Position:
    def __init__(self, fn, col=0, ln=0, idx=0):
        self.col = col
        self.ln = ln
        self.fn = fn
        self.idx = idx
    
    def advance(t=" "):
        for c in t:
            self.col += 1
            self.idx += 1
            if c == "\n":
                self.col = 0
                self.ln += 1
    
    def copy():
        return Position(self.fn, self.col, self.ln, self.idx)
    
    def __repr__():
        return f'column {self.col}, line {self.ln} in {self.fn}'