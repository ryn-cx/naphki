# TODO: Validate
"""Rebuilds VideoEpisodesModel."""

from __future__ import annotations

import logging

from get_around import build_client_automatically

from generate.constants import FILES_PATH, NAPHKI_PATH
from generate.utils import download_if_missing, load_ids, rebuild_model
from naphki import Naphki

PROGRAM_IDS = load_ids("VideoEpisodesModel")

LIMIT = 1
"""One episode a page, which is how the recorded pages were asked for."""


# TODO: Validate
def generate_video_episodes(client: Naphki) -> None:
    """Rebuild VideoEpisodesModel."""
    for program_id in PROGRAM_IDS:
        download_if_missing(
            FILES_PATH,
            "VideoEpisodesModel",
            program_id,
            lambda program_id=program_id: client.video_episodes.download(
                program_id,
                limit=LIMIT,
            ),
        )
    rebuild_model(FILES_PATH, NAPHKI_PATH, "VideoEpisodesModel")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_video_episodes(Naphki(build_client_automatically()))
