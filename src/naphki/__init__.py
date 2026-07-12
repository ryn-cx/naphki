# TODO: Validate
"""Contains the Naphki class."""

import time
from datetime import datetime
from logging import NullHandler, getLogger
from typing import Any

from get_around import GetAround

from naphki.exceptions import HTTPError
from naphki.shows_search import ShowsSearch
from naphki.video_episode import VideoEpisode
from naphki.video_episodes import VideoEpisodes
from naphki.video_programs import VideoPrograms

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Naphki:
    """NHK World API wrapper."""

    API_DOMAIN = "api.nhkworld.jp"
    BASE_API_URL = f"https://{API_DOMAIN}"

    def __init__(
        self,
        language: str = "en",
        timeout: int = 30,
        get_around_client: GetAround | None = None,
    ) -> None:
        """Initialize the Naphki client."""
        self.language = language
        self.timeout = timeout

        self.get_around_client = get_around_client or GetAround()

        self.video_episodes = VideoEpisodes(self)
        self.video_episode = VideoEpisode(self)
        self.video_programs = VideoPrograms(self)
        self.shows_search = ShowsSearch(self)

        super().__init__()

    def download(
        self,
        endpoint: str,
        params: dict[str, Any],
        base_url: str | None = None,
        *,
        json_body: dict[str, Any] | None = None,
        log_id: str,
    ) -> dict[str, Any]:
        """Downloads data from the API for a given endpoint."""
        url = f"{base_url or self.BASE_API_URL}/{endpoint}"

        operation = f"{url} ({log_id})"
        logger.debug("Downloading: %s", operation)
        start = time.monotonic()

        if json_body is not None:
            response = self.get_around_client.post(
                url=url,
                json=json_body,
                timeout=self.timeout,
            )
        else:
            response = self.get_around_client.get(
                url=url,
                params=params,
                timeout=self.timeout,
            )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f"Unexpected response status code: {response.status_code}"
            raise HTTPError(msg)

        logger.debug("Downloaded %s (%.4f s)", operation, time.monotonic() - start)

        output = response.json()
        output["naphki"] = {}
        output["naphki"]["url"] = url
        output["naphki"]["timestamp"] = (
            datetime.now().astimezone().isoformat().replace("+00:00", "Z")
        )
        output["naphki"]["params"] = params
        if json_body is not None:
            output["naphki"]["body"] = json_body

        return output
