# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from naphki.exceptions import HTTPError
from tests.utils import assert_error, download_and_save, parse_json

if TYPE_CHECKING:
    from naphki import Naphki
    from naphki.video_programs import VideoPrograms

PROGRAM_ID = "japanologyplus"
"""program_id of Japanology Plus."""
INVALID_PROGRAM_ID = "qwertyuiopasdfghjkl"


@pytest.fixture(scope="session")
def endpoint(client: Naphki) -> VideoPrograms:
    return client.video_programs


class TestVideoPrograms:
    def test_download(self, endpoint: VideoPrograms) -> None:
        download_and_save(
            endpoint,
            PROGRAM_ID,
            lambda: endpoint.download(PROGRAM_ID),
        )

    def test_parse(self, endpoint: VideoPrograms) -> None:
        data = parse_json(endpoint, PROGRAM_ID)
        assert data.id == PROGRAM_ID

    def test_invalid_download(self, endpoint: VideoPrograms) -> None:
        assert_error(
            endpoint,
            INVALID_PROGRAM_ID,
            lambda: endpoint.download(INVALID_PROGRAM_ID),
            HTTPError,
        )


@pytest.mark.parametrize("language", ["", "ja"])
def test_log_id(endpoint: VideoPrograms, language: str) -> None:
    expected = f"VideoPrograms program_id={PROGRAM_ID!r}"
    if language:
        expected += f" language={language!r}"
    assert endpoint.get_log_id(PROGRAM_ID, language) == expected
