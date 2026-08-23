# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from naphki.exceptions import ProgramNotFoundError
from naphki.video_program.models import VideoProgramModel
from tests.utils import RecordedEndpoint

if TYPE_CHECKING:
    from naphki import Naphki

PROGRAM_IDS = [
    # https://www3.nhk.or.jp/nhkworld/en/shows/japanologyplus/
    pytest.param("japanologyplus", id="japanology plus"),
]


# TODO: Validate
class VideoProgramTest(RecordedEndpoint):
    MODEL = VideoProgramModel
    # How many episodes, clips and casts are listed moves as they expire and
    # come back.
    SAME_TYPE = ("VideoEpisodes.total", "VideoClips.total", "Casts.total")


# TODO: Validate
@pytest.mark.parametrize("program_id", PROGRAM_IDS)
def test_download(client: Naphki, program_id: str) -> None:
    VideoProgramTest.download_test(
        program_id,
        lambda: client.video_program.download(program_id),
    )


# TODO: Validate
@pytest.mark.parametrize("program_id", PROGRAM_IDS)
def test_parse(client: Naphki, program_id: str) -> None:
    program = client.video_program.load(VideoProgramTest.recorded_content(program_id))
    assert program.id == program_id


# TODO: Validate
@pytest.mark.parametrize(
    "program_id",
    [pytest.param("qwertyuiopasdfghjkl", id="show that does not exist")],
)
def test_download_invalid(client: Naphki, program_id: str) -> None:
    VideoProgramTest.error_test(
        program_id,
        lambda: client.video_program.download(program_id),
        ProgramNotFoundError,
    )
