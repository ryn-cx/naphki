# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from naphki.shows_search.models import ShowsSearchModel
from tests.utils import RecordedEndpoint

if TYPE_CHECKING:
    from naphki import Naphki

SIZE = 3
"""A few results a page, so a page stays small enough to read."""

QUERIES = [
    pytest.param("japan", id="shows about japan"),
    pytest.param("qwertyuiopasdfghjkl", id="term nothing matches"),
]

HIT_COUNTS = [
    pytest.param("japan", SIZE, id="shows about japan"),
    pytest.param("qwertyuiopasdfghjkl", 0, id="term nothing matches"),
]


# TODO: Validate
class ShowsSearchTest(RecordedEndpoint):
    MODEL = ShowsSearchModel
    # How long the search took and how well each show scored move on their own.
    IGNORED = ("ShowsSearchModel.took",)
    SAME_TYPE = ("Hits.max_score", "Hit.field_score", "Total.value")


# TODO: Validate
@pytest.mark.parametrize("query", QUERIES)
def test_download(client: Naphki, query: str) -> None:
    ShowsSearchTest.download_test(
        query,
        lambda: client.shows_search.download(query, size=SIZE),
    )


# TODO: Validate
@pytest.mark.parametrize(("query", "hit_count"), HIT_COUNTS)
def test_parse(client: Naphki, query: str, hit_count: int) -> None:
    results = client.shows_search.load(ShowsSearchTest.recorded_content(query))
    assert len(results.hits.hits) == hit_count
