# TODO: Validate
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_no_content_error, data_path, download_if_missing

if TYPE_CHECKING:
    from pathlib import Path

    from naphki import Naphki
    from naphki.shows_search import ShowsSearch
    from naphki.shows_search.models import ShowsSearchModel

SEARCH_QUERY = "japan"
INVALID_SEARCH_QUERY = "qwertyuiopasdfghjklzxcvbnm"


@pytest.fixture(scope="session")
def endpoint(client: Naphki) -> ShowsSearch:
    return client.shows_search


@pytest.fixture(scope="session")
def json_file(endpoint: ShowsSearch) -> Path:
    return data_path(endpoint, SEARCH_QUERY)


@pytest.fixture(scope="session")
def data(endpoint: ShowsSearch, json_file: Path) -> ShowsSearchModel:
    return endpoint.parse(json.loads(json_file.read_text()))


class TestShowsSearch:
    def test_download(self, endpoint: ShowsSearch) -> None:
        download_if_missing(
            endpoint,
            SEARCH_QUERY,
            lambda: endpoint.download(SEARCH_QUERY),
        )

    def test_value(self, data: ShowsSearchModel) -> None:
        assert any(
            SEARCH_QUERY in hit.field_source.title.lower() for hit in data.hits.hits
        )

    def test_invalid(self, endpoint: ShowsSearch) -> None:
        name = INVALID_SEARCH_QUERY
        assert_no_content_error(
            endpoint,
            name,
            lambda: endpoint.get(INVALID_SEARCH_QUERY),
        )
