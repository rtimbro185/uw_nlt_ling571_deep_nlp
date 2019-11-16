class BaseException(Exception):
    def __init__(self,msg):
        self.msg = msg


class MainException(BaseException):
    def __abs__(self,msg):
        self.msg = msg

class ZeroParseException(BaseException):
    def __abs__(self,msg):
        self.msg = msg
