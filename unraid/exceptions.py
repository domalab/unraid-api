class UnraidAPIException(Exception):
    """Base exception for Unraid API errors."""

class ConnectionError(UnraidAPIException):
    """Raised when there's an error connecting to the Unraid server."""

class ExecutionError(UnraidAPIException):
    """Raised when a command execution fails."""

class ParseError(UnraidAPIException):
    """Raised when parsing command output fails."""