# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    def __init__(self, message):
        self.message = message


class Blocked(Error):
    """Raised when Blocked"""
    def __init__(self, message):
        super(Blocked, self).__init__(message)


class InvalidCredentials(Error):
    """Raised when InvalidCredentials"""
    def __init__(self, message):
        super(InvalidCredentials, self).__init__(message)


class ElementNotFound(Error):
    """Raised when ElementNotFound"""
    def __init__(self, message):
        super(ElementNotFound, self).__init__(message)