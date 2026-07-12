# TODO: Validate
"""Contains the ShowsSearch class."""

from __future__ import annotations

from typing import Any, override

from naphki.base_api_endpoint import BaseEndpoint
from naphki.shows_search.models import ShowsSearchModel


class ShowsSearch(BaseEndpoint[ShowsSearchModel]):
    """Manage the shows search file."""

    _response_model = ShowsSearchModel

    def download(self, query: str, *, from_: int = 0, size: int = 40) -> dict[str, Any]:
        """Downloads the shows search file."""
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
            log_id=f"{self.__class__.__name__} {query}",
        )

    @staticmethod
    @override
    def has_content(response: dict[str, Any]) -> bool:
        return bool(response["hits"]["hits"])

    def get(self, query: str) -> ShowsSearchModel:
        """Downloads and parses the shows search file.

        Raises:
            NoContentError: If the response has no meaningful content. The raw
                response is available on the exception's `response` attribute.
        """
        response = self.download(query)
        return self._parse_or_raise(response, f"{self.__class__.__name__} {query}")

    def get_all(self, query: str) -> list[ShowsSearchModel]:
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
