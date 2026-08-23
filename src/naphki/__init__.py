# TODO: Validate
"""Contains the Naphki class."""

import time
from http import HTTPStatus
from logging import NullHandler, getLogger
from typing import Any

from get_around import GetAround

from naphki.exceptions import HTTPError, ResourceNotFoundError
from naphki.shows_search import ShowsSearch
from naphki.video_episode import VideoEpisode
from naphki.video_episodes import VideoEpisodes
from naphki.video_program import VideoProgram

logger = getLogger(__name__)
logger.addHandler(NullHandler())


# TODO: Validate
class Naphki:
    """NHK World API wrapper."""

    # TODO: Validate
    def __init__(
        self,
        get_around_client: GetAround | None = None,
        language: str = "en",
        timeout: int = 30,
    ) -> None:
        """Initialize the Naphki client.

        The client holds one attribute per endpoint, so `client.video_program(id)`
        looks a show up and `client.video_program.download(id)` and
        `client.video_program.load(data)` are the halves of it.
        """
        self.language = language
        self.timeout = timeout
        self.get_around_client = get_around_client or GetAround()

        self.video_episodes = VideoEpisodes(self)
        self.video_episode = VideoEpisode(self)
        self.video_program = VideoProgram(self)
        self.shows_search = ShowsSearch(self)

    # TODO: Validate
    def download(
        self,
        endpoint: str,
        params: dict[str, Any],
        log_id: str,
        *,
        json_body: dict[str, Any] | None = None,
    ) -> str:
        """Download from the API and return the body as text.

        A request carrying a body is posted, and everything else is a GET.

        Raises:
            ResourceNotFoundError: If the API says the thing does not exist.
            HTTPError: If the request is answered with any other error.
        """
        logger.debug("Downloading: %s", log_id)
        url = f"https://api.nhkworld.jp/{endpoint}"
        start = time.monotonic()

        if json_body is None:
            response = self.get_around_client.get(
                url=url,
                params=params,
                timeout=self.timeout,
            )
        else:
            response = self.get_around_client.post(
                url=url,
                json=json_body,
                timeout=self.timeout,
            )

        if response.status_code != HTTPStatus.OK:
            # An id nothing is under is refused with a 404 for a show and a 400
            # for an episode.
            if response.status_code in {HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST}:
                raise ResourceNotFoundError(response.status_code, response.text)
            raise HTTPError(response.status_code, response.text)

        logger.debug("Downloaded %s (%.4f s)", log_id, time.monotonic() - start)
        return response.text
