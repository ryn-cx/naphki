# TODO: Validate
from __future__ import annotations

from typing import Any


class NaphkiError(Exception):
    """Base exception for naphki library."""


class HTTPError(NaphkiError):
    """Raised when HTTP request fails with unexpected status code."""


class NoContentError(NaphkiError):
    """Raised when a response has no meaningful content."""

    def __init__(
        self,
        response: dict[str, Any],
        log_id: str,
    ) -> None:
        """Store the downloaded response so it can be recovered by the caller."""
        self.response = response
        super().__init__(f"Response has no content for {log_id}.")
