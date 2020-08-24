from string_pointer import string_with_arrows

class Error:
    def __init__(self, _type, details, pos_start=None, pos_end=None):
        self.type = _type
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def __repr__(self):
        return f"Error: \x1b[31;1m{self.type}:\x1b[0m {self.details}"

class InvalidCharError(Error):
    def __init__(self, char, pos):
        super().__init__('InvalidCharError', f'Invalid character `{char}` at {pos}')

class InvalidTokenError(Error):
    def __init__(self, token):
        super().__init__('InvalidTokenError', f'Unexpected token `{token.value}` at {token.pos_start}')

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

class OperationError(ox_Exception):
    def __init__(self, token, _type, message, ctx):
        super().__init__('OperationError', f'Failed to apply operator {token.value} to {_type}: {message}', token.pos_start, token.pos_end, ctx)

class VarCreateException(ox_Exception):
    def __init__(self, message, pstart, pend, ctx):
        super().__init__('VarCreationException', f'Failed to create variable: {message}', pstart, pend, ctx)

class VarAssignmentException(ox_Exception):
    def __init__(self, message, pstart, pend, ctx):
        super().__init__('VarAssignmentException', f'Failed to assign variable: {message}', pstart, pend, ctx)