# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from naphki.exceptions import HTTPError
from tests.utils import assert_error, download_and_save, parse_json

if TYPE_CHECKING:
    from naphki import Naphki
    from naphki.video_episode import VideoEpisode

EPISODE_ID = 5001461
"""episode_id of a single video episode."""
INVALID_EPISODE_ID = 1


@pytest.fixture(scope="session")
def endpoint(client: Naphki) -> VideoEpisode:
    return client.video_episode


class TestVideoEpisode:
    def test_download(self, endpoint: VideoEpisode) -> None:
        download_and_save(
            endpoint,
            str(EPISODE_ID),
            lambda: endpoint.download(EPISODE_ID),
        )

    def test_parse(self, endpoint: VideoEpisode) -> None:
        data = parse_json(endpoint, str(EPISODE_ID))
        assert data.id == str(EPISODE_ID)

    def test_invalid_download(self, endpoint: VideoEpisode) -> None:
        assert_error(
            endpoint,
            str(INVALID_EPISODE_ID),
            lambda: endpoint.download(INVALID_EPISODE_ID),
            HTTPError,
        )


@pytest.mark.parametrize("language", ["", "ja"])
def test_log_id(endpoint: VideoEpisode, language: str) -> None:
    expected = f"VideoEpisode episode_id={EPISODE_ID!r}"
    if language:
        expected += f" language={language!r}"
    assert endpoint.get_log_id(EPISODE_ID, language) == expected
