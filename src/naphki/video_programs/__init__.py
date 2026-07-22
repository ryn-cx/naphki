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

    def download(self, program_id: str, language: str = "") -> dict[str, Any]:
        """Downloads the video programs file."""
        log_id = self.get_log_id(self.download, locals())
        resolved_language = language or self._client.language
        endpoint = f"showsapi/v1/{resolved_language}/video_programs/{program_id}"
        return self._client.download(
            endpoint,
            {},
            log_id=log_id,
        )

    def download_and_parse(
        self,
        program_id: str,
        language: str = "",
    ) -> VideoProgramsModel:
        """Downloads and parses the video programs file."""
        return self.parse(self.download(program_id, language))
