# TODO: Validate
import json
from datetime import UTC, datetime, timedelta

import pytest
from get_around import build_client_automatically

from naphki import Naphki
from naphki.exceptions import NoContentError

client = Naphki(build_client_automatically())

EPISODES_PROGRAM_ID = "dwc"
"""program_id used to filter video episodes to a single show."""
INVALID_PROGRAM_ID = "qwertyuiopasdfghjkl"


class TestVideoEpisodes:
    def test_get(self) -> None:
        endpoint = client.video_episodes
        model = endpoint.get()
        assert model.items
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_for_program(self) -> None:
        endpoint = client.video_episodes
        model = endpoint.get(EPISODES_PROGRAM_ID)
        assert all(item.video_program.id == EPISODES_PROGRAM_ID for item in model.items)
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_for_program_all_pages(self) -> None:
        endpoint = client.video_episodes
        pages = endpoint.get_all(EPISODES_PROGRAM_ID)
        assert pages
        items = sum(len(page.items) for page in pages)
        assert items == pages[0].pagination.total

    def test_get_to_datetime(self) -> None:
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

    def test_invalid_get(self) -> None:
        with pytest.raises(NoContentError) as error:
            client.video_episodes.get(INVALID_PROGRAM_ID)
        assert "items" in error.value.response

    def test_parse(self) -> None:
        endpoint = client.video_episodes
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))
