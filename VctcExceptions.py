class VctcException(Exception):
    def __init__(self,message,code):
        super().__init__(code+":"+message)
        self.message=message
        self.code=code