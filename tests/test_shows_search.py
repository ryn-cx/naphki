# TODO: Validate
import json

import pytest
from get_around import build_client_automatically

from naphki import Naphki
from naphki.exceptions import NoContentError

client = Naphki(build_client_automatically())

SEARCH_QUERY = "japan"
INVALID_SEARCH_QUERY = "qwertyuiopasdfghjklzxcvbnm"


class TestShowsSearch:
    def test_get(self) -> None:
        endpoint = client.shows_search
        model = endpoint.get(SEARCH_QUERY)
        assert any(
            SEARCH_QUERY in hit.field_source.title.lower() for hit in model.hits.hits
        )
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_all_pages(self) -> None:
        endpoint = client.shows_search
        pages = endpoint.get_all(SEARCH_QUERY)
        assert len(pages) > 1
        hits = sum(len(page.hits.hits) for page in pages)
        assert hits == pages[0].hits.total.value

    def test_invalid_get(self) -> None:
        with pytest.raises(NoContentError) as error:
            client.shows_search.get(INVALID_SEARCH_QUERY)
        assert "hits" in error.value.response

    def test_parse(self) -> None:
        endpoint = client.shows_search
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))
