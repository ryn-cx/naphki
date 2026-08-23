# TODO: Validate
"""Helpers for putting a downloaded response where the generator reads it."""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

logger = logging.getLogger(__name__)


# TODO: Validate
def sanitized_file_name(name: str | int) -> str:
    """Turn a name into a file name that is valid on Windows."""
    sanitized = re.compile(r'[<>:"/\|?*\x00-\x1f]').sub("_", str(name)).rstrip(". ")
    return sanitized or "_"


# TODO: Validate
def download_if_missing(
    files_path: Path,
    model_name: str,
    name: str | int,
    download: Callable[[], str],
) -> None:
    """Download a response into `_files` when it is not recorded yet."""
    recorded_path = files_path / model_name / f"{sanitized_file_name(name)}.json"
    if recorded_path.exists():
        return
    logger.info("Downloading %s/%s.", model_name, name)
    recorded_path.parent.mkdir(parents=True, exist_ok=True)
    recorded_path.write_text(download())
