# TODO: Validate
"""Exceptions."""


class NaphkiError(Exception):
    """Base exception for naphki library."""


class HTTPError(NaphkiError):
    """Raised when HTTP request fails with unexpected status code."""
