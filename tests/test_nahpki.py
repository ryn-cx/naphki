# TODO: Validate
"""Tests."""

import json
from datetime import UTC, datetime, timedelta

from naphki import Naphki

client = Naphki()


class TestGet:
    """Test live get requests across every endpoint."""

    def test_get_video_episodes(self) -> None:
        """Test getting video episodes."""
        model = client.video_episodes.get()
        client.video_episodes.save_new_json_file(client.video_episodes.original_input(model))

    def test_get_video_episodes_for_program(self) -> None:
        """Test getting a single show's video episodes."""
        model = client.video_episodes.get("dwc")
        client.video_episodes.save_new_json_file(client.video_episodes.original_input(model))

    def test_get_video_episodes_for_program_all_pages(self) -> None:
        """Test getting every page of a single show's video episodes."""
        pages = client.video_episodes.get_all("dwc")
        assert pages
        items = sum(len(page.items) for page in pages)
        assert items == pages[0].pagination.total

    def test_get_video_episodes_to_datetime(self) -> None:
        """Test get_all stops at an inclusive published_at cutoff."""
        cutoff = datetime.now(tz=UTC) - timedelta(days=5)
        pages = client.video_episodes.get_all(to_datetime=cutoff)
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
        """Test getting a single video episode."""
        model = client.video_episode.get(5001461)
        client.video_episode.save_new_json_file(client.video_episode.original_input(model))

    def test_get_video_programs(self) -> None:
        """Test getting a single video program."""
        model = client.video_programs.get("japanologyplus")
        client.video_programs.save_new_json_file(client.video_programs.original_input(model))

    def test_get_shows_search(self) -> None:
        """Test searching for shows."""
        model = client.shows_search.get("japan")
        client.shows_search.save_new_json_file(client.shows_search.original_input(model))

    def test_get_shows_search_all_pages(self) -> None:
        """Test getting every page of a shows search."""
        pages = client.shows_search.get_all("japan")
        assert len(pages) > 1
        hits = sum(len(page.hits.hits) for page in pages)
        assert hits == pages[0].hits.total.value


class TestParse:
    """Test parsing every saved file for each endpoint."""

    def test_parse_video_episodes(self) -> None:
        """Test parsing video episodes files."""
        for json_file in client.video_episodes.json_files():
            client.video_episodes.parse(json.loads(json_file.read_text()))

    def test_parse_video_episode(self) -> None:
        """Test parsing video episode files."""
        for json_file in client.video_episode.json_files():
            client.video_episode.parse(json.loads(json_file.read_text()))

    def test_parse_video_programs(self) -> None:
        """Test parsing video programs files."""
        for json_file in client.video_programs.json_files():
            client.video_programs.parse(json.loads(json_file.read_text()))

    def test_parse_shows_search(self) -> None:
        """Test parsing shows search files."""
        for json_file in client.shows_search.json_files():
            client.shows_search.parse(json.loads(json_file.read_text()))
