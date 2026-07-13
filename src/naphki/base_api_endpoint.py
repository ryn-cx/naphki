# TODO: Validate
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from good_ass_pydantic_integrator import GAPIBaseModel, GAPIClient

from naphki.constants import FILES_PATH
from naphki.exceptions import NoContentError

if TYPE_CHECKING:
    from naphki import Naphki


class BaseExtractor[T: GAPIBaseModel](GAPIClient[T]):
    """Base class to extract data from API responses."""

    JSON_FILES_ROOT = FILES_PATH


class BaseEndpoint[T: GAPIBaseModel](BaseExtractor[T]):
    """Base class for API endpoints."""

    def __init__(self, client: Naphki) -> None:
        """Initialize the endpoint with the Naphki client."""
        self._client = client

    @staticmethod
    @abstractmethod
    def has_content(*args: Any, **kwargs: Any) -> bool:  # noqa: ANN401
        """Return whether the response has meaningful content."""

    def _parse_or_raise(self, response: dict[str, Any], log_id: str) -> T:
        """Parse `response`, or raise `NoContentError` if it is empty.

        Raises:
            NoContentError: If `has_content` is false.
        """
        if not self.has_content(response):
            raise NoContentError(response, log_id)
        return self.parse(response)
