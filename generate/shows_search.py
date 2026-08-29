# TODO: Validate
"""Rebuilds ShowsSearchModel."""

from __future__ import annotations

import logging

from get_around import build_client_automatically

from generate.constants import FILES_PATH, NAPHKI_PATH
from generate.utils import download_if_missing, load_ids, rebuild_model
from naphki import Naphki

QUERIES = load_ids("ShowsSearchModel")

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
    rebuild_model(FILES_PATH, NAPHKI_PATH, "ShowsSearchModel")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_shows_search(Naphki(build_client_automatically()))
