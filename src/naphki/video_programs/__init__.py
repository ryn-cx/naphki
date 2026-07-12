# TODO: Validate
"""Contains the VideoPrograms class."""

from __future__ import annotations

from typing import Any, override

from naphki.base_api_endpoint import BaseEndpoint
from naphki.video_programs.models import VideoProgramsModel


class VideoPrograms(BaseEndpoint[VideoProgramsModel]):
    """Manage the video programs file."""

    _response_model = VideoProgramsModel

    def download(self, program_id: str, language: str = "") -> dict[str, Any]:
        """Downloads the video programs file."""
        language = language or self._client.language
        endpoint = f"showsapi/v1/{language}/video_programs/{program_id}"
        return self._client.download(
            endpoint,
            {},
            log_id=f"{self.__class__.__name__} {program_id}",
        )

    @staticmethod
    @override
    def has_content(response: dict[str, Any]) -> bool:
        return bool(response["id"])

    def get(self, program_id: str, language: str = "") -> VideoProgramsModel:
        """Downloads and parses the video programs file.

        Raises:
            NoContentError: If the response has no meaningful content. The raw
                response is available on the exception's `response` attribute.
        """
        response = self.download(program_id, language)
        return self._parse_or_raise(response, f"{self.__class__.__name__} {program_id}")
