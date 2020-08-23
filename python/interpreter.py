class RTResult:
    def __init__(self):
        self.error = None
        self.value = None
    
    def failure(self, error):
        self.error = error
        return self
    
    def success(self, value):
        #print('Succeded with', value)
        self.value = value
        return self
    
    def register(self, res):
        #print(f"\x1b[32mpassed" + ('\x1b[31;1m' if res == None else ''), res, "\x1b[0m")
        if res.error:
            self.error = res.error
            return self
        return res.value