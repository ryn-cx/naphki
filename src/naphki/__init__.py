# TODO: Validate
"""Naphki is a client for downloading and parsing data from NHK World."""

from datetime import datetime
from typing import Any

from get_around import GetAround

from naphki.exceptions import HTTPError
from naphki.shows_search import ShowsSearch
from naphki.video_episode import VideoEpisode
from naphki.video_episodes import VideoEpisodes
from naphki.video_programs import VideoPrograms



class Naphki:
    """Interface for downloading and parsing data from NHK World."""

    API_DOMAIN = "api.nhkworld.jp"
    BASE_API_URL = f"https://{API_DOMAIN}"

    def __init__(
        self,
        language: str = "en",
        timeout: int = 30,
        get_around_server: str | None = None,
        get_around_password: str | None = None,
    ) -> None:
        """Initialize the Naphki client."""
        self.language = language
        self.timeout = timeout

        self.get_around_client = GetAround(
            server=get_around_server,
            password=get_around_password,
        )

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
    ) -> dict[str, Any]:
        """Downloads data from the API for a given endpoint.

        Sends a GET request, or a POST request when ``json_body`` is provided.
        """
        url = f"{base_url or self.BASE_API_URL}/{endpoint}"

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

        # PLR2004 - 200 represents the status code "200 OK".
        if response.status_code != 200:  # noqa: PLR2004
            msg = f"Unexpected response status code: {response.status_code}"
            raise HTTPError(msg)

        output = response.json()
        output["naphki"] = {}
        output["naphki"]["url"] = url
        output["naphki"]["timestamp"] = datetime.now().astimezone().isoformat().replace("+00:00", "Z")
        output["naphki"]["params"] = params
        if json_body is not None:
            output["naphki"]["body"] = json_body

        return output
