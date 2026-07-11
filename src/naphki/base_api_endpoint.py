# TODO: Validate
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, override

from good_ass_pydantic_integrator import GAPIBaseModel, GAPIClient

from naphki.constants import FILES_PATH
from naphki.exceptions import NoContentError

if TYPE_CHECKING:
    from pathlib import Path

    from naphki import Naphki


class BaseExtractor[T: GAPIBaseModel](GAPIClient[T]):
    """Base class to extract data from API responses."""

    @override
    @classmethod
    def json_files_folder(cls) -> Path:
        folder_name = cls._folder_name(cls._model_name())
        return FILES_PATH / folder_name


class BaseEndpoint[T: GAPIBaseModel](BaseExtractor[T]):
    """Base class for API endpoints."""

    def __init__(self, client: Naphki) -> None:
        """Initialize the endpoint with the Naphki client."""
        self._client = client

    @staticmethod
    @abstractmethod
    def has_content(*args: Any, **kwargs: Any) -> bool:  # noqa: ANN401
        """Return whether the response has meaningful content."""

    def _parse_or_raise(self, response: dict[str, Any], *, has_content: bool) -> T:
        """Parse `response`, or raise `NoContentError` when it is empty.

        This is the single place `get` decides "nothing here". The raised
        `NoContentError` carries `response`, so callers can still recover the
        downloaded payload from the exception.

        Args:
            response: The raw JSON response to parse.
            has_content: The endpoint's `has_content` verdict for `response`.

        Returns:
            The parsed model.

        Raises:
            NoContentError: If `has_content` is false.
        """
        if not has_content:
            raise NoContentError(response, endpoint=type(self).__name__)
        return self.parse(response)
