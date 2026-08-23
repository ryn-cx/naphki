# TODO: Validate
"""Rebuilds VideoEpisodeModel."""

from __future__ import annotations

import logging

from get_around import build_client_automatically
from good_ass_pydantic_integrator import generate_model

from generate.constants import FILES_PATH, NAPHKI_PATH
from generate.utils import download_if_missing
from naphki import Naphki

EPISODE_IDS = [5001461]


# TODO: Validate
def generate_video_episode(client: Naphki) -> None:
    """Rebuild VideoEpisodeModel."""
    for episode_id in EPISODE_IDS:
        download_if_missing(
            FILES_PATH,
            "VideoEpisodeModel",
            episode_id,
            lambda episode_id=episode_id: client.video_episode.download(episode_id),
        )
    generate_model(FILES_PATH, NAPHKI_PATH, "VideoEpisodeModel")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_video_episode(Naphki(build_client_automatically()))
