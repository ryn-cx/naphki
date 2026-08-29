# TODO: Validate
"""Contains the VideoEpisode class."""

from __future__ import annotations

import json
from http import HTTPStatus
from logging import NullHandler, getLogger

from naphki.base_api_endpoint import BaseEndpoint
from naphki.exceptions import EpisodeNotFoundError, ResourceNotFoundError
from naphki.video_episode.models import VideoEpisodeModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())


# TODO: Validate
class VideoEpisode(BaseEndpoint):
    """Manage the video episode file.

    Source: https://www3.nhk.or.jp/nhkworld/en/shows/{episode_id}/

    Example request:
        - GET /showsapi/v1/en/video_episodes/{episode_id}?
            - schedule=True
            - HTTP/2
        - Host: api.nhkworld.jp
        - User-Agent: __REDACTED__
        - Accept: application/json
        - Accept-Language: en-US,en;q=0.9
        - Accept-Encoding: gzip, deflate, br, zstd
        - Connection: keep-alive
        - Referer: https://www3.nhk.or.jp/nhkworld/en/shows/{episode_id}/
        - Sec-Fetch-Dest: empty
        - Sec-Fetch-Mode: cors
        - Sec-Fetch-Site: cross-site
    """

    # TODO: Validate
    def __call__(self, episode_id: int, language: str = "") -> VideoEpisodeModel:
        """Look the episode up and return the model it is read into."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(self.download(episode_id, language), log_id)

    # TODO: Validate
    def download(self, episode_id: int, language: str = "") -> str:
        """Download the video episode file."""
        log_id = self.get_log_id(self.download, locals())
        resolved_language = language or self._client.language
        try:
            response = self._client.download(
                endpoint=f"showsapi/v1/{resolved_language}/video_episodes/{episode_id}",
                params={"schedule": True},
                log_id=log_id,
            )
        except ResourceNotFoundError as err:
            raise EpisodeNotFoundError(
                episode_id,
                err.status_code,
                err.response,
            ) from err
        return self._validate_download(response, episode_id)

    # TODO: Validate
    def _validate_download(self, response: str, episode_id: int) -> str:
        if json.loads(response).get("id") != str(episode_id):
            raise EpisodeNotFoundError(episode_id, HTTPStatus.OK, response)
        return response

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> VideoEpisodeModel:
        """Read a downloaded video episode file into its model."""
        return model_validate_json(data, log_id or self.default_log_id)
