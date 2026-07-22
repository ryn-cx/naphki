# TODO: Validate
"""Contains the VideoEpisodes class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import TYPE_CHECKING, Any

from naphki.base_api_endpoint import BaseEndpoint
from naphki.video_episodes.models import VideoEpisodesModel

if TYPE_CHECKING:
    from datetime import datetime

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class VideoEpisodes(BaseEndpoint[VideoEpisodesModel]):
    """Manage the video episodes file."""

    _response_model = VideoEpisodesModel

    def download(
        self,
        program_id: str | None = None,
        *,
        limit: int = 20,
        offset: int = 0,
        language: str = "",
    ) -> dict[str, Any]:
        """Downloads the video episodes file."""
        log_id = self.get_log_id(self.download, locals())
        resolved_language = language or self._client.language
        if program_id is None:
            endpoint = f"showsapi/v1/{resolved_language}/video_episodes"
        else:
            endpoint = (
                f"showsapi/v1/{resolved_language}"
                f"/video_programs/{program_id}/video_episodes"
            )
        params: dict[str, str | int] = {"limit": limit, "offset": offset}
        return self._client.download(
            endpoint,
            params,
            log_id=log_id,
        )

    def download_and_parse(
        self,
        program_id: str | None = None,
        *,
        limit: int = 20,
        offset: int = 0,
        language: str = "",
    ) -> VideoEpisodesModel:
        """Downloads and parses the video episodes file."""
        return self.parse(
            self.download(
                program_id,
                limit=limit,
                offset=offset,
                language=language,
            ),
        )

    def download_and_parse_all(
        self,
        program_id: str | None = None,
        *,
        to_datetime: datetime | None = None,
        language: str = "",
    ) -> list[VideoEpisodesModel]:
        """Downloads and parses every page of video episodes.

        Repeatedly calls ``download_and_parse()``, advancing through the
        pagination until all episodes have been retrieved.

        Episodes are returned newest first (by ``video.published_at``). When
        ``to_datetime`` is given, scraping stops once an episode published at or
        before it is reached, so only episodes published on or after
        ``to_datetime`` are guaranteed to be collected.

        Args:
            program_id: A program (show) ID to limit results to a single show, e.g.
                ``"dwc"``. When omitted, every video episode is returned.
            to_datetime: The inclusive, timezone-aware datetime to scrape back to,
                compared against each episode's ``video.published_at``.
            language: The language code to use for the request.

        Returns:
            A list of VideoEpisodesModel, one per page.
        """
        pages: list[VideoEpisodesModel] = []
        offset = 0
        while True:
            page = self.download_and_parse(
                program_id,
                offset=offset,
                language=language,
            )
            pages.append(page)
            offset += page.pagination.count

            reached_datetime = to_datetime is not None and any(
                item.video.published_at <= to_datetime for item in page.items
            )
            if (
                page.pagination.next is None
                or page.pagination.count == 0
                or reached_datetime
            ):
                break
        return pages
