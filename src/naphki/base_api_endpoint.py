# TODO: Validate
"""Base API endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from good_ass_pydantic_integrator import GAPIBaseModel, GAPIClient

from naphki.constants import FILES_PATH

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
