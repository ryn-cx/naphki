# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from naphki.exceptions import EpisodeNotFoundError
from naphki.video_episode.models import VideoEpisodeModel
from tests.utils import RecordedEndpoint

if TYPE_CHECKING:
    from naphki import Naphki

EPISODE_IDS = [
    # https://www3.nhk.or.jp/nhkworld/en/shows/5001461/
    pytest.param(5001461, id="100 years of osaka - midosuji line architecture"),
]


# TODO: Validate
class VideoEpisodeTest(RecordedEndpoint):
    MODEL = VideoEpisodeModel
    # The stream is re-issued with a new address and a new expiry every so often.
    SAME_TYPE = ("Video.url", "Video.analytics", "Video.expired_at")


# TODO: Validate
@pytest.mark.parametrize("episode_id", EPISODE_IDS)
def test_download(client: Naphki, episode_id: int) -> None:
    VideoEpisodeTest.download_test(
        episode_id,
        lambda: client.video_episode.download(episode_id),
    )


# TODO: Validate
@pytest.mark.parametrize("episode_id", EPISODE_IDS)
def test_parse(client: Naphki, episode_id: int) -> None:
    episode = client.video_episode.load(VideoEpisodeTest.recorded_content(episode_id))
    assert episode.id == str(episode_id)


# TODO: Validate
@pytest.mark.parametrize(
    "episode_id",
    [pytest.param(1, id="episode that does not exist")],
)
def test_download_invalid(client: Naphki, episode_id: int) -> None:
    VideoEpisodeTest.error_test(
        episode_id,
        lambda: client.video_episode.download(episode_id),
        EpisodeNotFoundError,
    )
