# TODO: Validate
"""Contains the ShowsSearch class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import Any

from naphki.base_api_endpoint import BaseEndpoint
from naphki.shows_search.models import ShowsSearchModel

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class ShowsSearch(BaseEndpoint[ShowsSearchModel]):
    """Manage the shows search file."""

    _response_model = ShowsSearchModel

    def download(self, query: str, *, from_: int = 0, size: int = 40) -> dict[str, Any]:
        """Downloads the shows search file."""
        log_id = self.get_log_id(self.download, locals())
        index = f"nhkworld@{self._client.language}@ondemand@vod@programs"
        endpoint = f"nwapi/showssearch/v1/{index}/list.json"
        body: dict[str, Any] = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": query,
                                "type": "cross_fields",
                                "fields": ["title^16", "description^1"],
                                "operator": "and",
                            },
                        },
                        {
                            "multi_match": {
                                "query": query,
                                "type": "cross_fields",
                                "fields": ["body^1"],
                                "operator": "and",
                            },
                        },
                    ],
                },
            },
            "from": from_,
            "size": size,
            "_source": ["title", "description", "slug", "url", "thumbnail"],
        }
        return self._client.download(
            endpoint,
            {},
            json_body=body,
            log_id=log_id,
        )

    def download_and_parse(self, query: str) -> ShowsSearchModel:
        """Downloads and parses the shows search file."""
        return self.parse(self.download(query))

    def download_and_parse_all(self, query: str) -> list[ShowsSearchModel]:
        """Searches for shows and parses every page of results.

        Repeatedly searches, advancing through the result set until every match
        has been retrieved.

        Args:
            query: The search term, e.g. ``"japan"``.

        Returns:
            A list of ShowsSearchModel, one per page.
        """
        pages: list[ShowsSearchModel] = []
        from_ = 0
        while True:
            page = self.parse(self.download(query, from_=from_))
            pages.append(page)
            from_ += len(page.hits.hits)
            if from_ >= page.hits.total.value or not page.hits.hits:
                break
        return pages
