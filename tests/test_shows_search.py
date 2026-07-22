# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import download_and_save, parse_json

if TYPE_CHECKING:
    from naphki import Naphki
    from naphki.shows_search import ShowsSearch

SEARCH_QUERY = "japan"


@pytest.fixture(scope="session")
def endpoint(client: Naphki) -> ShowsSearch:
    return client.shows_search


class TestShowsSearch:
    def test_download(self, endpoint: ShowsSearch) -> None:
        download_and_save(
            endpoint,
            SEARCH_QUERY,
            lambda: endpoint.download(SEARCH_QUERY),
        )

    def test_parse(self, endpoint: ShowsSearch) -> None:
        data = parse_json(endpoint, SEARCH_QUERY)
        assert any(
            SEARCH_QUERY in hit.field_source.title.lower() for hit in data.hits.hits
        )
