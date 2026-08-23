# TODO: Validate
"""Rebuilds VideoProgramModel."""

from __future__ import annotations

import logging

from get_around import build_client_automatically
from good_ass_pydantic_integrator import generate_model

from generate.constants import FILES_PATH, NAPHKI_PATH
from generate.utils import download_if_missing
from naphki import Naphki

PROGRAM_IDS = ["japanologyplus"]


# TODO: Validate
def generate_video_program(client: Naphki) -> None:
    """Rebuild VideoProgramModel."""
    for program_id in PROGRAM_IDS:
        download_if_missing(
            FILES_PATH,
            "VideoProgramModel",
            program_id,
            lambda program_id=program_id: client.video_program.download(program_id),
        )
    generate_model(FILES_PATH, NAPHKI_PATH, "VideoProgramModel")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_video_program(Naphki(build_client_automatically()))
