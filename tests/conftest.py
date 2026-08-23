# TODO: Validate
import pytest
from get_around import build_client_automatically

from naphki import Naphki


# TODO: Validate
@pytest.fixture(scope="session")
def client() -> Naphki:
    return Naphki(build_client_automatically())
