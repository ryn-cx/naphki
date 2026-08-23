# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from naphki.video_episodes.models import VideoEpisodesModel
from tests.utils import RecordedEndpoint

if TYPE_CHECKING:
    from naphki import Naphki

LIMIT = 1
"""One episode a page, so a page stays small enough to read."""

PROGRAM_IDS = [
    # https://www3.nhk.or.jp/nhkworld/en/shows/dwc/
    pytest.param("dwc", id="dining with the chef"),
    pytest.param("qwertyuiopasdfghjkl", id="show that does not exist"),
]


# TODO: Validate
class VideoEpisodesTest(RecordedEndpoint):
    MODEL = VideoEpisodesModel
    # The stream is re-issued with a new address and a new expiry every so often.
    SAME_TYPE = ("Video.url", "Video.analytics", "Video.expired_at", "Pagination.next")
    # Episodes are added over time, so the count only grows.
    LESS_THAN_OR_EQUAL = ("Pagination.total",)


# TODO: Validate
@pytest.mark.parametrize("program_id", PROGRAM_IDS)
def test_download(client: Naphki, program_id: str) -> None:
    VideoEpisodesTest.download_test(
        program_id,
        lambda: client.video_episodes.download(program_id, limit=LIMIT),
    )


# TODO: Validate
@pytest.mark.parametrize("program_id", PROGRAM_IDS)
def test_parse(client: Naphki, program_id: str) -> None:
    page = client.video_episodes.load(VideoEpisodesTest.recorded_content(program_id))
    assert all(item.video_program.id == program_id for item in page.items)
