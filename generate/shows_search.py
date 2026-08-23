# TODO: Validate
"""Rebuilds ShowsSearchModel."""

from __future__ import annotations

import logging

from get_around import build_client_automatically
from good_ass_pydantic_integrator import generate_model

from generate.constants import FILES_PATH, NAPHKI_PATH
from generate.utils import download_if_missing
from naphki import Naphki

QUERIES = ["japan", "qwertyuiopasdfghjkl"]

SIZE = 3
"""A few results a page, which is how the recorded pages were asked for."""


# TODO: Validate
def generate_shows_search(client: Naphki) -> None:
    """Rebuild ShowsSearchModel."""
    for query in QUERIES:
        download_if_missing(
            FILES_PATH,
            "ShowsSearchModel",
            query,
            lambda query=query: client.shows_search.download(query, size=SIZE),
        )
    generate_model(FILES_PATH, NAPHKI_PATH, "ShowsSearchModel")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_shows_search(Naphki(build_client_automatically()))
