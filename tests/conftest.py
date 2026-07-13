# TODO: Validate
import pytest
from get_around import build_client_automatically

from naphki import Naphki


@pytest.fixture(scope="session")
def client() -> Naphki:
    return Naphki(get_around_client=build_client_automatically())
