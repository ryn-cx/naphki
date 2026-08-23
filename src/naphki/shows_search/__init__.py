# TODO: Validate
"""Contains the ShowsSearch class."""

from __future__ import annotations

import json
from logging import NullHandler, getLogger
from typing import Any

from naphki.base_api_endpoint import BaseEndpoint
from naphki.shows_search.models import ShowsSearchModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())

SIZE = 40


# TODO: Validate
class ShowsSearch(BaseEndpoint):
    """Manage the shows search file.

    The search is an Elasticsearch query posted as the site sends it.

    Source: https://www3.nhk.or.jp/nhkworld/en/shows/search/?q={query}

    Example request:
        - POST /nwapi/showssearch/v1/{index}/list.json
            - HTTP/2
        - Host: api.nhkworld.jp
        - User-Agent: __REDACTED__
        - Accept: application/json
        - Accept-Language: en-US,en;q=0.9
        - Accept-Encoding: gzip, deflate, br, zstd
        - Content-Type: application/json
        - Connection: keep-alive
        - Referer: https://www3.nhk.or.jp/nhkworld/en/shows/search/?q={query}
        - Sec-Fetch-Dest: empty
        - Sec-Fetch-Mode: cors
        - Sec-Fetch-Site: cross-site
    """

    # TODO: Validate
    def __call__(
        self,
        query: str,
        *,
        from_: int = 0,
        size: int = SIZE,
    ) -> ShowsSearchModel:
        """Run the search and return the model it is read into."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(self.download(query, from_=from_, size=size), log_id)

    # TODO: Validate
    def download(self, query: str, *, from_: int = 0, size: int = SIZE) -> str:
        """Download the shows search file.

        Args:
            query: The search term, e.g. `"japan"`.
            from_: Where in the whole run of results to start.
            size: How many results to ask for.
        """
        log_id = self.get_log_id(self.download, locals())
        index = f"nhkworld@{self._client.language}@ondemand@vod@programs"
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
            f"nwapi/showssearch/v1/{index}/list.json",
            params={},
            log_id=log_id,
            json_body=body,
        )

    # TODO: Validate
    def download_all(self, query: str, *, size: int = SIZE) -> list[str]:
        """Download every page of results a search matches."""
        pages: list[str] = []
        from_ = 0

        while True:
            page = self.download(query, from_=from_, size=size)
            pages.append(page)

            hits = json.loads(page)["hits"]
            from_ += len(hits["hits"])
            if not hits["hits"] or from_ >= hits["total"]["value"]:
                return pages

    # TODO: Validate
    def download_merged(self, query: str, *, size: int = SIZE) -> str:
        """Download every page of results a search matches as a single file.

        The pages are put together into one file holding every hit, which is the
        whole result set written the way one page of it is, rather than the
        pages themselves.
        """
        return self.merge_pages(self.download_all(query, size=size))

    # TODO: Validate
    @staticmethod
    def merge_pages(pages: list[str]) -> str:
        """Return the pages of one search written out as a single file.

        The first page is what the merged file is built on, since its total is
        how many the search matched, and its hits are replaced by the hits of
        every page in the order they were served.

        Raises:
            ValueError: If there are no pages, since there is nothing to say the
                search was answered with.
        """
        if not pages:
            msg = "Expected at least one page, got none."
            raise ValueError(msg)

        documents: list[dict[str, Any]] = [json.loads(page) for page in pages]
        merged = json.loads(pages[0])
        merged["hits"]["hits"] = [
            hit for document in documents for hit in document["hits"]["hits"]
        ]
        return json.dumps(merged)

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> ShowsSearchModel:
        """Read a downloaded shows search file into its model."""
        return model_validate_json(data, log_id or type(self).__name__)

    # TODO: Validate
    def load_pages(self, datas: list[str]) -> list[ShowsSearchModel]:
        """Read the pages `download_all` returns into their models."""
        return [self.load(data) for data in datas]
