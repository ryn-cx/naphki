# TODO: Validate
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_http_error, data_path, download_if_missing

if TYPE_CHECKING:
    from pathlib import Path

    from naphki import Naphki
    from naphki.video_episode import VideoEpisode
    from naphki.video_episode.models import VideoEpisodeModel

EPISODE_ID = 5001461
"""episode_id of a single video episode."""
INVALID_EPISODE_ID = 1


@pytest.fixture(scope="session")
def endpoint(client: Naphki) -> VideoEpisode:
    return client.video_episode


@pytest.fixture(scope="session")
def json_file(endpoint: VideoEpisode) -> Path:
    return data_path(endpoint, str(EPISODE_ID))


@pytest.fixture(scope="session")
def data(endpoint: VideoEpisode, json_file: Path) -> VideoEpisodeModel:
    return endpoint.parse(json.loads(json_file.read_text()))


class TestVideoEpisode:
    def test_download(self, endpoint: VideoEpisode) -> None:
        download_if_missing(
            endpoint,
            str(EPISODE_ID),
            lambda: endpoint.download(EPISODE_ID),
        )

    def test_value(self, data: VideoEpisodeModel) -> None:
        assert data.id == str(EPISODE_ID)

    def test_invalid(self, endpoint: VideoEpisode) -> None:
        name = str(INVALID_EPISODE_ID)
        assert_http_error(
            endpoint,
            name,
            lambda: endpoint.download(INVALID_EPISODE_ID),
        )
