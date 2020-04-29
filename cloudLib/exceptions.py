"""Exceptions for crownstone lib connection lib"""
from enum import Enum


class AuthError(Enum):
    LOGIN_FAILED = 'LOGIN_FAILED'
    USERNAME_EMAIL_REQUIRED = 'USERNAME_EMAIL_REQUIRED'
    LOGIN_FAILED_EMAIL_NOT_VERIFIED = 'LOGIN_FAILED_EMAIL_NOT_VERIFIED'
    AUTHORIZATION_REQUIRED = 'AUTHORIZATION_REQUIRED'


class CrownstoneAuthenticationError(Exception):
    """Raised when authentication with API ended in error"""
    type = None
    message = None

    def __init__(self, type, message=None):
        self.type = type
        self.message = message


class CrownstoneUnknownError(Exception):
    """Raised when the error is not known / no data"""
