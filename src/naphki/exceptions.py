# TODO: Validate
"""Exceptions."""

from __future__ import annotations

from typing import Any


# TODO: Validate
class NaphkiError(Exception):
    """Base exception for Naphki."""

    response: str | dict[str, Any] | None = None


# TODO: Validate
class HTTPError(NaphkiError):
    """Raised when HTTP request fails with unexpected status code."""

    # TODO: Validate
    def __init__(
        self,
        status_code: int,
        response: str | dict[str, Any] | None,
    ) -> None:
        """Initialize the HTTPError with the status code and response body."""
        self.status_code = status_code
        self.response = response
        super().__init__(f"Unexpected response status code: {status_code}")


# TODO: Validate
class ResourceNotFoundError(HTTPError):
    """Raised when the API reports that the requested resource does not exist."""


# TODO: Validate
class EpisodeNotFoundError(ResourceNotFoundError):
    """Raised when the requested episode does not exist."""

    # TODO: Validate
    def __init__(
        self,
        episode_id: int,
        status_code: int,
        response: str | dict[str, Any] | None,
    ) -> None:
        """Initialize with the episode id and the originating response."""
        self.episode_id = episode_id
        super().__init__(status_code, response)


# TODO: Validate
class ProgramNotFoundError(ResourceNotFoundError):
    """Raised when the requested show does not exist."""

    # TODO: Validate
    def __init__(
        self,
        program_id: str,
        status_code: int,
        response: str | dict[str, Any] | None,
    ) -> None:
        """Initialize with the show id and the originating response."""
        self.program_id = program_id
        super().__init__(status_code, response)
