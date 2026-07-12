# TODO: Validate
import json

import pytest
from get_around import build_client_automatically

from naphki import Naphki
from naphki.exceptions import HTTPError

client = Naphki(build_client_automatically())

EPISODE_ID = 5001461
"""episode_id of a single video episode."""
INVALID_EPISODE_ID = 1


class TestVideoEpisode:
    def test_get(self) -> None:
        endpoint = client.video_episode
        model = endpoint.get(EPISODE_ID)
        assert model.id == str(EPISODE_ID)
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_invalid_get(self) -> None:
        with pytest.raises(HTTPError):
            client.video_episode.get(INVALID_EPISODE_ID)

    def test_parse(self) -> None:
        endpoint = client.video_episode
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))
