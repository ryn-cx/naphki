# TODO: Validate
"""Contains the VideoPrograms class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import Any

from naphki.base_api_endpoint import BaseEndpoint
from naphki.video_programs.models import VideoProgramsModel

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class VideoPrograms(BaseEndpoint[VideoProgramsModel]):
    """Manage the video programs file."""

    _response_model = VideoProgramsModel

    def get_log_id(self, program_id: str, language: str = "") -> str:
        """Build the log id for a download."""
        return self.append_non_default_args(
            f"{self.__class__.__name__} {program_id=}",
            language=(language, ""),
        )

    def download(self, program_id: str, language: str = "") -> dict[str, Any]:
        """Downloads the video programs file."""
        resolved_language = language or self._client.language
        endpoint = f"showsapi/v1/{resolved_language}/video_programs/{program_id}"
        return self._client.download(
            endpoint,
            {},
            log_id=self.get_log_id(program_id, language),
        )

    def download_and_parse(
        self,
        program_id: str,
        language: str = "",
    ) -> VideoProgramsModel:
        """Downloads and parses the video programs file."""
        return self.parse(self.download(program_id, language))
