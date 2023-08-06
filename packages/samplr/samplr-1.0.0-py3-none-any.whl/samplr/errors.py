class LimitrError(Exception):
    pass

class SamplrValueError(LimitrError):
    pass

class SamplrTypeError(LimitrError):
    pass

class InvalidFunctionError(LimitrError):
    pass
