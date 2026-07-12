# TODO: Validate
"""Contains the VideoEpisode class."""

from __future__ import annotations

from typing import Any, override

from naphki.base_api_endpoint import BaseEndpoint
from naphki.video_episode.models import VideoEpisodeModel


class VideoEpisode(BaseEndpoint[VideoEpisodeModel]):
    """Manage the video episode file."""

    _response_model = VideoEpisodeModel

    def download(self, episode_id: int, language: str = "") -> dict[str, Any]:
        """Downloads the video episode file."""
        language = language or self._client.language
        endpoint = f"showsapi/v1/{language}/video_episodes/{episode_id}"
        params: dict[str, str | int | bool] = {"schedule": True}
        return self._client.download(
            endpoint,
            params,
            log_id=f"{self.__class__.__name__} {episode_id}",
        )

    @staticmethod
    @override
    def has_content(response: dict[str, Any]) -> bool:
        return bool(response["id"])

    def get(self, episode_id: int, language: str = "") -> VideoEpisodeModel:
        """Downloads and parses the video episode file.

        Raises:
            NoContentError: If the response has no meaningful content. The raw
                response is available on the exception's `response` attribute.
        """
        response = self.download(episode_id, language)
        return self._parse_or_raise(response, f"{self.__class__.__name__} {episode_id}")
