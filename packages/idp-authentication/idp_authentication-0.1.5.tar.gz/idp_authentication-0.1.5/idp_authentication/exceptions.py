from dataclasses import dataclass


@dataclass
class ExceptionBase(Exception):
    """Base class for all exceptions in this module."""

    message: str

    def __str__(self):
        return self.message


@dataclass
class AccessDenied(ExceptionBase):
    """Raised when a user is not allowed to access a resource."""

    message: str = "Access denied"


@dataclass
class UserNotFound(ExceptionBase):
    """Raised when a user is not found."""

    def __init__(self, username: str):
        self.message = f"User with username={username} not found!"
