class Position:
    def __init__(self, fn, txt="", col=0, ln=0, idx=0):
        self.txt = txt
        self.col = col
        self.ln = ln
        self.fn = fn
        self.idx = idx
    
    def advance(self, t=" "):
        for c in t:
            self.col += 1
            self.idx += 1
            if c == "\n":
                self.col = 0
                self.ln += 1
    
    def copy(self):
        return Position(self.fn, self.txt, self.col, self.ln, self.idx)
    
    def __repr__(self):
        return f'column {self.col}, line {self.ln} in {self.fn}'