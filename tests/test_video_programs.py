# TODO: Validate
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_http_error, data_path, download_if_missing

if TYPE_CHECKING:
    from pathlib import Path

    from naphki import Naphki
    from naphki.video_programs import VideoPrograms
    from naphki.video_programs.models import VideoProgramsModel

PROGRAM_ID = "japanologyplus"
"""program_id of Japanology Plus."""
INVALID_PROGRAM_ID = "qwertyuiopasdfghjkl"


@pytest.fixture(scope="session")
def endpoint(client: Naphki) -> VideoPrograms:
    return client.video_programs


@pytest.fixture(scope="session")
def json_file(endpoint: VideoPrograms) -> Path:
    return data_path(endpoint, PROGRAM_ID)


@pytest.fixture(scope="session")
def data(endpoint: VideoPrograms, json_file: Path) -> VideoProgramsModel:
    return endpoint.parse(json.loads(json_file.read_text()))


class TestVideoPrograms:
    def test_download(self, endpoint: VideoPrograms) -> None:
        download_if_missing(
            endpoint,
            PROGRAM_ID,
            lambda: endpoint.download(PROGRAM_ID),
        )

    def test_value(self, data: VideoProgramsModel) -> None:
        assert data.id == PROGRAM_ID

    def test_invalid(self, endpoint: VideoPrograms) -> None:
        name = INVALID_PROGRAM_ID
        assert_http_error(
            endpoint,
            name,
            lambda: endpoint.download(INVALID_PROGRAM_ID),
        )
