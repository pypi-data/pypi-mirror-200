class CanadaPostException(Exception):
    def __init__(self, code, description):
        self.code = code
        self.description = description
        self.message = "[%s] %s" % (self.code, self.description)


class CanadaPostThrottleException(CanadaPostException):
    pass
