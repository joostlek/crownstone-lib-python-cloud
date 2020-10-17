"""Exceptions for crownstone cloud connection cloud"""

AuthError = {
    'LOGIN_FAILED': 'Wrong email or password provided',
    'USERNAME_EMAIL_REQUIRED': 'Email or password not provided',
    'LOGIN_FAILED_EMAIL_NOT_VERIFIED': 'Email has not been verified, please do that first',
}

DataError = {
    'DOES_NOT_EXIST': 'Data does not exist',
    'ALREADY_EXISTS': 'Data already exists'
}


class CrownstoneException(Exception):
    """Raised when authentication with API ended in error"""
    exception_type = None
    message = None

    def __init__(self, exception_type, message=None):
        self.type = exception_type
        self.message = message


class CrownstoneAuthenticationError(CrownstoneException):
    """Raised when authentication with API ended in error"""


class CrownstoneUnknownError(Exception):
    """Raised when the error is not known / no data"""


class CrownstoneConnectionError(Exception):
    """Raised when a connection to the Crownstone Cloud can't be made."""


class CrownstoneDataError(CrownstoneException):
    """Raised when an object is not found in a dictionary containing Crownstone data."""
