# TODO: Validate
"""Video episode API endpoint."""

from __future__ import annotations

from typing import Any, override

from naphki.base_api_endpoint import BaseEndpoint
from naphki.video_episode.models import VideoEpisodeModel


class VideoEpisode(BaseEndpoint[VideoEpisodeModel]):
    """Provides methods to download, parse, and retrieve a single video episode."""

    _response_model = VideoEpisodeModel

    def download(self, episode_id: int, language: str = "") -> dict[str, Any]:
        """Downloads a single video episode.

        Args:
            episode_id: The episode ID, e.g. ``5001461``.
            language: The language code to use for the request.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        language = language or self._client.language
        endpoint = f"showsapi/v1/{language}/video_episodes/{episode_id}"
        params: dict[str, str | int | bool] = {"schedule": True}
        return self._client.download(endpoint, params)

    @staticmethod
    @override
    def has_content(response: dict[str, Any]) -> bool:
        return bool(response["id"])

    def get(self, episode_id: int, language: str = "") -> VideoEpisodeModel:
        """Downloads and parses a single video episode.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            episode_id: The episode ID, e.g. ``5001461``.
            language: The language code to use for the request.

        Returns:
            A VideoEpisodeModel containing the parsed data.

        Raises:
            NoContentError: If the response has no meaningful content. The raw
                response is available on the exception's `response` attribute.
        """
        response = self.download(episode_id, language)
        return self._parse_or_raise(response, has_content=self.has_content(response))
