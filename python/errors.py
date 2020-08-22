class Error:
    def __init__(self, _type, details):
        self.type = _type
        self.details = details
    
    def __repr__(self):
        return f"Error: \x1b[31;1m{self.type}:\x1b[0m {self.details}"

class InvalidCharError(Error):
    def __init__(self, char, pos):
        super().__init__('InvalidCharError', f'Invalid character `{char}` at {pos}')