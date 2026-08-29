# TODO: Validate
"""Contains the VideoEpisodes class."""

from __future__ import annotations

import json
from datetime import datetime
from logging import NullHandler, getLogger
from typing import Any

from naphki.base_api_endpoint import BaseEndpoint
from naphki.video_episodes.models import VideoEpisodesModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())

LIMIT = 20


# TODO: Validate
class VideoEpisodes(BaseEndpoint):
    """Manage the video episodes file.

    Source: https://www3.nhk.or.jp/nhkworld/en/shows/{program_id}/

    Example request:
        - GET /showsapi/v1/en/video_programs/{program_id}/video_episodes?
            - limit=20&
            - offset=0
            - HTTP/2
        - Host: api.nhkworld.jp
        - User-Agent: __REDACTED__
        - Accept: application/json
        - Accept-Language: en-US,en;q=0.9
        - Accept-Encoding: gzip, deflate, br, zstd
        - Connection: keep-alive
        - Referer: https://www3.nhk.or.jp/nhkworld/en/shows/{program_id}/
        - Sec-Fetch-Dest: empty
        - Sec-Fetch-Mode: cors
        - Sec-Fetch-Site: cross-site
    """

    # TODO: Validate
    def __call__(
        self,
        program_id: str | None = None,
        *,
        limit: int = LIMIT,
        offset: int = 0,
        language: str = "",
    ) -> VideoEpisodesModel:
        """Look a page of episodes up and return the model it is read into."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(
            self.download(
                program_id,
                limit=limit,
                offset=offset,
                language=language,
            ),
            log_id,
        )

    # TODO: Validate
    def download(
        self,
        program_id: str | None = None,
        *,
        limit: int = LIMIT,
        offset: int = 0,
        language: str = "",
    ) -> str:
        """Download the video episodes file.

        Args:
            program_id: A show to limit the page to, e.g. `"dwc"`. Left out, the
                page is of every show's episodes.
            limit: How many episodes to ask for.
            offset: Where in the whole run of them to start.
            language: The language to ask in, defaulting to the client's.
        """
        log_id = self.get_log_id(self.download, locals())
        resolved_language = language or self._client.language
        if program_id is None:
            endpoint = f"showsapi/v1/{resolved_language}/video_episodes"
        else:
            endpoint = (
                f"showsapi/v1/{resolved_language}"
                f"/video_programs/{program_id}/video_episodes"
            )
        return self._client.download(
            endpoint,
            params={"limit": limit, "offset": offset},
            log_id=log_id,
        )

    # TODO: Validate
    def download_until_datetime(
        self,
        program_id: str | None = None,
        end_datetime: datetime | None = None,
        *,
        limit: int = LIMIT,
        language: str = "",
    ) -> list[str]:
        """Download pages of episodes until end_datetime is reached.

        Episodes come back newest first, so the walk stops on the page holding
        the first episode published at or before end_datetime.
        """
        pages: list[str] = []
        offset = 0

        while True:
            page = self.download(
                program_id,
                limit=limit,
                offset=offset,
                language=language,
            )
            pages.append(page)

            parsed = json.loads(page)
            offset += parsed["pagination"]["count"]
            reached_datetime = end_datetime is not None and any(
                datetime.fromisoformat(item["video"]["published_at"]) <= end_datetime
                for item in parsed["items"]
            )
            if (
                parsed["pagination"]["next"] is None
                or parsed["pagination"]["count"] == 0
                or reached_datetime
            ):
                return pages

    # TODO: Validate
    def download_merged_until_datetime(
        self,
        program_id: str | None = None,
        end_datetime: datetime | None = None,
        *,
        limit: int = LIMIT,
        language: str = "",
    ) -> str:
        """Download every page down to `end_datetime` as a single file.

        The pages are put together into one file holding every episode the walk
        reached, which is that stretch of the listing written the way one page
        of it is, rather than the pages themselves.
        """
        return self.merge_pages(
            self.download_until_datetime(
                program_id,
                end_datetime,
                limit=limit,
                language=language,
            ),
        )

    # TODO: Validate
    @staticmethod
    def merge_pages(pages: list[str]) -> str:
        """Return the pages of one listing written out as a single file.

        The first page is what the merged file is built on and its items are
        replaced by the items of every page in the order they were served. The
        pagination is rewritten to cover every item gathered and to point
        nowhere, since a file holding the whole walk is not a page of anything.

        Raises:
            ValueError: If there are no pages, since there is nothing to say the
                listing was answered with.
        """
        if not pages:
            msg = "Expected at least one page, got none."
            raise ValueError(msg)

        documents: list[dict[str, Any]] = [json.loads(page) for page in pages]
        merged = json.loads(pages[0])
        merged["items"] = [item for document in documents for item in document["items"]]
        merged["pagination"]["count"] = len(merged["items"])
        merged["pagination"]["next"] = None
        return json.dumps(merged)

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> VideoEpisodesModel:
        """Read a downloaded video episodes file into its model."""
        return model_validate_json(data, log_id or self.default_log_id)

    # TODO: Validate
    def load_pages(self, datas: list[str]) -> list[VideoEpisodesModel]:
        """Read the pages `download_until_datetime` returns into their models."""
        return [self.load(data) for data in datas]
