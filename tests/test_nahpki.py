# TODO: Validate
from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import pytest
from get_around import build_client_automatically

from naphki import Naphki
from naphki.exceptions import HTTPError, NoContentError

client = Naphki(build_client_automatically())

SEARCH_QUERY = "japan"
EPISODE_ID = 5001461
"""episode_id of a single video episode."""
PROGRAM_ID = "japanologyplus"
"""program_id of Japanology Plus."""
EPISODES_PROGRAM_ID = "dwc"
"""program_id used to filter video episodes to a single show."""
INVALID_EPISODE_ID = 1
INVALID_PROGRAM_ID = "qwertyuiopasdfghjkl"
INVALID_SEARCH_QUERY = "qwertyuiopasdfghjklzxcvbnm"


class TestGet:
    def test_get_video_episodes(self) -> None:
        endpoint = client.video_episodes
        model = endpoint.get()
        assert model.items
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_video_episodes_for_program(self) -> None:
        endpoint = client.video_episodes
        model = endpoint.get(EPISODES_PROGRAM_ID)
        assert all(
            item.video_program.id == EPISODES_PROGRAM_ID for item in model.items
        )
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_video_episodes_for_program_all_pages(self) -> None:
        endpoint = client.video_episodes
        pages = endpoint.get_all(EPISODES_PROGRAM_ID)
        assert pages
        items = sum(len(page.items) for page in pages)
        assert items == pages[0].pagination.total

    def test_get_video_episodes_to_datetime(self) -> None:
        endpoint = client.video_episodes
        cutoff = datetime.now(tz=UTC) - timedelta(days=5)
        pages = endpoint.get_all(to_datetime=cutoff)
        assert pages
        items = [item for page in pages for item in page.items]
        # Scraped back to at least the cutoff.
        assert min(item.video.published_at for item in items) <= cutoff
        # Stopped early instead of fetching every page.
        total = pages[0].pagination.total
        page_size = pages[0].pagination.limit
        full_pages = (total + page_size - 1) // page_size
        assert len(pages) < full_pages

    def test_get_video_episode(self) -> None:
        endpoint = client.video_episode
        model = endpoint.get(EPISODE_ID)
        assert model.id == str(EPISODE_ID)
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_video_programs(self) -> None:
        endpoint = client.video_programs
        model = endpoint.get(PROGRAM_ID)
        assert model.id == PROGRAM_ID
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_shows_search(self) -> None:
        endpoint = client.shows_search
        model = endpoint.get(SEARCH_QUERY)
        assert any(
            SEARCH_QUERY in hit.field_source.title.lower()
            for hit in model.hits.hits
        )
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_shows_search_all_pages(self) -> None:
        endpoint = client.shows_search
        pages = endpoint.get_all(SEARCH_QUERY)
        assert len(pages) > 1
        hits = sum(len(page.hits.hits) for page in pages)
        assert hits == pages[0].hits.total.value


class TestInvalidGet:
    def test_invalid_get_video_episodes(self) -> None:
        with pytest.raises(NoContentError) as error:
            client.video_episodes.get(INVALID_PROGRAM_ID)
        assert "items" in error.value.response

    def test_invalid_get_video_episode(self) -> None:
        with pytest.raises(HTTPError):
            client.video_episode.get(INVALID_EPISODE_ID)

    def test_invalid_get_video_programs(self) -> None:
        with pytest.raises(HTTPError):
            client.video_programs.get(INVALID_PROGRAM_ID)

    def test_invalid_get_shows_search(self) -> None:
        with pytest.raises(NoContentError) as error:
            client.shows_search.get(INVALID_SEARCH_QUERY)
        assert "hits" in error.value.response


class TestParse:
    @pytest.mark.parametrize(
        "endpoint_name",
        ["video_episodes", "video_episode", "video_programs", "shows_search"],
    )
    def test_parse(self, endpoint_name: str) -> None:
        endpoint = getattr(client, endpoint_name)
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))
