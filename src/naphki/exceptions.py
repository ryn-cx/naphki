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
        *,
        endpoint: str | None = None,
    ) -> None:
        """Store the downloaded response so it can be recovered by the caller.

        Args:
            response: The raw JSON response that was found to be empty.
            endpoint: The endpoint name, included in the error message.
        """
        self.response = response
        location = f" for {endpoint}" if endpoint else ""
        super().__init__(f"Response has no content{location}.")
