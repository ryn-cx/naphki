# TODO: Validate
import json

import pytest
from get_around import build_client_automatically

from naphki import Naphki
from naphki.exceptions import HTTPError

client = Naphki(build_client_automatically())

PROGRAM_ID = "japanologyplus"
"""program_id of Japanology Plus."""
INVALID_PROGRAM_ID = "qwertyuiopasdfghjkl"


class TestVideoPrograms:
    def test_get(self) -> None:
        endpoint = client.video_programs
        model = endpoint.get(PROGRAM_ID)
        assert model.id == PROGRAM_ID
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_invalid_get(self) -> None:
        with pytest.raises(HTTPError):
            client.video_programs.get(INVALID_PROGRAM_ID)

    def test_parse(self) -> None:
        endpoint = client.video_programs
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))
