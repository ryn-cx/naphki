# TODO: Validate
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_no_content_error, data_path, download_if_missing

if TYPE_CHECKING:
    from pathlib import Path

    from naphki import Naphki
    from naphki.video_episodes import VideoEpisodes
    from naphki.video_episodes.models import VideoEpisodesModel

EPISODES_PROGRAM_ID = "dwc"
"""program_id used to filter video episodes to a single show."""
INVALID_PROGRAM_ID = "qwertyuiopasdfghjkl"


@pytest.fixture(scope="session")
def endpoint(client: Naphki) -> VideoEpisodes:
    return client.video_episodes


@pytest.fixture(scope="session")
def json_file(endpoint: VideoEpisodes) -> Path:
    return data_path(endpoint, EPISODES_PROGRAM_ID)


@pytest.fixture(scope="session")
def data(endpoint: VideoEpisodes, json_file: Path) -> VideoEpisodesModel:
    return endpoint.parse(json.loads(json_file.read_text()))


class TestVideoEpisodes:
    def test_download(self, endpoint: VideoEpisodes) -> None:
        download_if_missing(
            endpoint,
            EPISODES_PROGRAM_ID,
            lambda: endpoint.download(EPISODES_PROGRAM_ID),
        )

    def test_value(self, data: VideoEpisodesModel) -> None:
        assert all(
            item.video_program.id == EPISODES_PROGRAM_ID for item in data.items
        )

    def test_invalid(self, endpoint: VideoEpisodes) -> None:
        name = INVALID_PROGRAM_ID
        assert_no_content_error(
            endpoint,
            name,
            lambda: endpoint.get(INVALID_PROGRAM_ID),
        )
