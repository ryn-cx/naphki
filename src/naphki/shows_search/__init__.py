# TODO: Validate
"""Shows search API endpoint."""

from __future__ import annotations

from typing import Any, override

from naphki.base_api_endpoint import BaseEndpoint
from naphki.shows_search.models import ShowsSearchModel


class ShowsSearch(BaseEndpoint[ShowsSearchModel]):
    """Provides methods to search for shows (video programs)."""

    _response_model = ShowsSearchModel

    def download(self, query: str, *, from_: int = 0, size: int = 40) -> dict[str, Any]:
        """Searches for shows (video programs) matching a search term.

        Args:
            query: The search term, e.g. ``"japan"``.
            from_: The number of results to skip (for pagination).
            size: The number of results to return.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
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
        return self._client.download(endpoint, {}, json_body=body)

    @staticmethod
    @override
    def has_content(response: dict[str, Any]) -> bool:
        return bool(response["hits"]["hits"])

    def get(self, query: str) -> ShowsSearchModel:
        """Searches for shows and parses the result.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            query: The search term, e.g. ``"japan"``.

        Returns:
            A ShowsSearchModel containing the parsed search results.

        Raises:
            NoContentError: If the response has no meaningful content. The raw
                response is available on the exception's `response` attribute.
        """
        response = self.download(query)
        return self._parse_or_raise(response, has_content=self.has_content(response))

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
