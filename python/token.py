class Token:
    def __init__(self, _type, value, pos_start, pos_end):
        self.type = _type
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def __eq__(self, r):
        if isinstance(r, str):
            return self.type == r
        if not isinstance(r, Token):
            return False
        return self.type == r.type
    
    def __gt__(self, r):
        if isinstance(r, str):
            return self.value == r
        if not isinstance(r, Token):
            return False
        return self.value == r.value
    
    def __lt__(self, s):
        if not isinstance(s, str):
            return False
        return f'{self.type}:{self.value}' == s

    def __repr__(self):
        return f'<{self.type}:{self.value}>'