# TODO: Validate
"""Contains BaseEndpoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from good_ass_pydantic_integrator import GAPIBaseModel, GAPIClient

from naphki.constants import FILES_PATH

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
    def append_non_default_args(
        log_id: str,
        **args: tuple[object, object],
    ) -> str:
        """Append ``name=value`` for each arg whose value differs from its default."""
        for name, (value, default) in args.items():
            if value != default:
                log_id += f" {name}={value!r}"
        return log_id
