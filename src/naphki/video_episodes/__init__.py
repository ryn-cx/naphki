# TODO: Validate
"""Video episodes API endpoint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from naphki.base_api_endpoint import BaseEndpoint
from naphki.video_episodes.models import VideoEpisodesModel

if TYPE_CHECKING:
    from datetime import datetime


class VideoEpisodes(BaseEndpoint[VideoEpisodesModel]):
    """Provides methods to download, parse, and retrieve video episode data.

    With no ``program_id`` this covers every video episode
    (``GET /video_episodes``). With a ``program_id`` it covers the episodes of a
    single show (``GET /video_programs/{program_id}/video_episodes``).
    """

    _response_model = VideoEpisodesModel

    def download(
        self,
        program_id: str | None = None,
        *,
        limit: int = 20,
        offset: int = 0,
        language: str = "",
    ) -> dict[str, Any]:
        """Downloads a page of video episodes.

        Args:
            program_id: A program (show) ID to limit results to a single show, e.g.
                ``"dwc"``. When omitted, every video episode is returned.
            limit: The maximum number of episodes to return.
            offset: The number of episodes to skip.
            language: The language code to use for the request.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        language = language or self._client.language
        if program_id is None:
            endpoint = f"showsapi/v1/{language}/video_episodes"
        else:
            endpoint = (
                f"showsapi/v1/{language}/video_programs/{program_id}/video_episodes"
            )
        params: dict[str, str | int] = {"limit": limit, "offset": offset}
        return self._client.download(endpoint, params)

    @staticmethod
    @override
    def has_content(response: dict[str, Any]) -> bool:
        return bool(response["items"])

    def get(
        self,
        program_id: str | None = None,
        *,
        limit: int = 20,
        offset: int = 0,
        language: str = "",
    ) -> VideoEpisodesModel:
        """Downloads and parses a page of video episodes.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            program_id: A program (show) ID to limit results to a single show, e.g.
                ``"dwc"``. When omitted, every video episode is returned.
            limit: The maximum number of episodes to return.
            offset: The number of episodes to skip.
            language: The language code to use for the request.

        Returns:
            A VideoEpisodesModel containing the parsed data.

        Raises:
            NoContentError: If the response has no meaningful content. The raw
                response is available on the exception's `response` attribute.
        """
        response = self.download(
            program_id,
            limit=limit,
            offset=offset,
            language=language,
        )
        return self._parse_or_raise(response, has_content=self.has_content(response))

    def get_all(
        self,
        program_id: str | None = None,
        *,
        to_datetime: datetime | None = None,
        language: str = "",
    ) -> list[VideoEpisodesModel]:
        """Downloads and parses every page of video episodes.

        Repeatedly calls ``get()``, advancing through the pagination until all
        episodes have been retrieved.

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
            page = self.get(
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
