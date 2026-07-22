# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import download_and_save, parse_json

if TYPE_CHECKING:
    from naphki import Naphki
    from naphki.video_episodes import VideoEpisodes

EPISODES_PROGRAM_ID = "dwc"
"""program_id used to filter video episodes to a single show."""


@pytest.fixture(scope="session")
def endpoint(client: Naphki) -> VideoEpisodes:
    return client.video_episodes


class TestVideoEpisodes:
    def test_download(self, endpoint: VideoEpisodes) -> None:
        download_and_save(
            endpoint,
            EPISODES_PROGRAM_ID,
            lambda: endpoint.download(EPISODES_PROGRAM_ID),
        )

    def test_parse(self, endpoint: VideoEpisodes) -> None:
        data = parse_json(endpoint, EPISODES_PROGRAM_ID)
        assert all(item.video_program.id == EPISODES_PROGRAM_ID for item in data.items)
