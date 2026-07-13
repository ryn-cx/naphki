# TODO: Validate
"""Utils."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from naphki.constants import FILES_PATH
from naphki.exceptions import HTTPError, NoContentError

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

TEST_FILES_DIRECTORY = FILES_PATH / "tests"


def data_path(endpoint: object, name: str) -> Path:
    """Return the path a file is saved at."""
    return TEST_FILES_DIRECTORY / type(endpoint).__name__ / f"{name}.json"


def download_if_missing(
    endpoint: object,
    name: str,
    download: Callable[[], object],
) -> Path:
    """Download the test file if it is missing."""
    path = data_path(endpoint, name)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(download(), indent=2))
    assert path.exists()
    return path


def assert_http_error(
    endpoint: object,
    name: str,
    download: Callable[[], object],
) -> None:
    """Assert that download raises HTTPError."""
    if data_path(endpoint, name).exists():
        pytest.skip(f"error already recorded for {type(endpoint).__name__}/{name}")
    with pytest.raises(HTTPError):
        download()
    record_error(endpoint, name)


def assert_no_content_error(
    endpoint: object,
    name: str,
    download: Callable[[], object],
) -> None:
    """Assert that download raises NoContentError."""
    if data_path(endpoint, name).exists():
        pytest.skip(f"error already recorded for {type(endpoint).__name__}/{name}")
    with pytest.raises(NoContentError):
        download()
    record_error(endpoint, name)


def record_error(endpoint: object, name: str) -> None:
    """Record error."""
    path = data_path(endpoint, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("")
