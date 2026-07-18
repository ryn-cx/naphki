# TODO: Validate
"""Contains the VideoEpisode class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import Any

from naphki.base_api_endpoint import BaseEndpoint
from naphki.video_episode.models import VideoEpisodeModel

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class VideoEpisode(BaseEndpoint[VideoEpisodeModel]):
    """Manage the video episode file."""

    _response_model = VideoEpisodeModel

    def get_log_id(self, episode_id: int, language: str = "") -> str:
        """Build the log id for a download."""
        return self.append_non_default_args(
            f"{self.__class__.__name__} {episode_id=}",
            language=(language, ""),
        )

    def download(self, episode_id: int, language: str = "") -> dict[str, Any]:
        """Downloads the video episode file."""
        resolved_language = language or self._client.language
        endpoint = f"showsapi/v1/{resolved_language}/video_episodes/{episode_id}"
        params: dict[str, str | int | bool] = {"schedule": True}
        return self._client.download(
            endpoint,
            params,
            log_id=self.get_log_id(episode_id, language),
        )

    def download_and_parse(
        self,
        episode_id: int,
        language: str = "",
    ) -> VideoEpisodeModel:
        """Downloads and parses the video episode file."""
        return self.parse(self.download(episode_id, language))
