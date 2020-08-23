class Error:
    def __init__(self, _type, details):
        self.type = _type
        self.details = details
    
    def __repr__(self):
        return f"Error: \x1b[31;1m{self.type}:\x1b[0m {self.details}"

class InvalidCharError(Error):
    def __init__(self, char, pos):
        super().__init__('InvalidCharError', f'Invalid character `{char}` at {pos}')

class InvalidTokenError(Error):
    def __init__(self, token):
        super().__init__('InvalidTokenError', f'Unexpected {token.value} at {token.pos_start}')

class ExpectedTokenError(Error):
    def __init__(self, token, pos_start):
        super().__init__('ExpectedTokenError', f'Expected {token} at {pos_start}')

class ox_Exception(Error): # Base class for runtime exceptions
    def __init__(self, type, details, pos_start, pos_end, context):
        super().__init__(f'Exception \x1b[34;1m{type}\x1b[31;1m', details, pos_start, pos_end)
        self.context = context
    
    def __repr__(self):
        result = self.create_traceback()
        result += f'\x1b[31;1m{self.type}\x1b[0m: {self.details}'
        result += '\n' + string_with_arrows(self.pos_start.txt, self.pos_start, self.pos_end)
        return result
    
    def create_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'\tFile {pos.fn}, line {str(pos.ln+1)} in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        return 'Traceback (most recent call last):\n' + result

class AssignmentException(ox_Exception):
    def __init__(self, token, _type, ctx):
        super().__init__('AssignmentException', f'Value {token.value} is not compatible with type {_type}', token.pos_start, token.pos_end, ctx)