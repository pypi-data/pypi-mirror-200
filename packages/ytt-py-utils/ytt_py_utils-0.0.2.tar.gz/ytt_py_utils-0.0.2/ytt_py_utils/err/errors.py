"""
Errors Utils
"""
class Error(Exception):
    """Base class for other exceptions"""
    pass


class ViewNotFoundError(Error):
    """Raised when the input value is too small"""
    pass

class MissingEnvironmentVariable(Error):
    """Raised when the input value is too small"""
    pass