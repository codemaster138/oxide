class RTResult:
    def __init__(self, returned=False):
        self.error = None
        self.value = None
        self.returned = returned
    
    def failure(self, error):
        self.error = error
        return self
    
    def success(self, value):
        #print('Succeded with', value)
        self.value = value
        return self
    
    def register(self, res):
        #print(f"\x1b[32mpassed" + ('\x1b[31;1m' if res == None else ''), res, "\x1b[0m")
        if res.returned: self.returned = res.returned
        if res.error:
            self.error = res.error
            return res.value
        return res.value

#################################
#            CONTEXT            #
#################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None
        self.func = False
        if parent:
            self.func = parent.func