"""Utils."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from naphki.constants import FILES_PATH

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
    from typing import Any

    from good_ass_pydantic_integrator import GAPIBaseModel, GAPIClient

    from naphki.base_api_endpoint import BaseEndpoint


def get_json_path(
    endpoint: GAPIClient[Any],
    name: str,
    *,
    folder: str | None = None,
) -> Path:
    if folder is not None:
        return FILES_PATH / folder / f"{name}.json"
    return endpoint.json_files_folder() / f"{name}.json"


def parse_json[T: GAPIBaseModel](endpoint: BaseEndpoint[T], name: str) -> T:
    json_path = get_json_path(endpoint, name)
    return endpoint.parse(json.loads(json_path.read_text()))


# The loaders below produce each input shape that an ``extract`` helper accepts,
# so extraction tests can parametrize over a single ``load`` callable.
def single_dict(endpoint: BaseEndpoint[Any], name: str) -> dict[str, Any]:
    """A single recorded page as a raw dict."""
    return json.loads(get_json_path(endpoint, name).read_text())


def page_dicts(
    endpoint: BaseEndpoint[Any],
    name: str,
    *,
    folder: str | None = None,
) -> list[dict[str, Any]]:
    """Recorded page(s) as a list of raw dicts, wrapping a single page."""
    content: list[dict[str, Any]] | dict[str, Any] = json.loads(
        get_json_path(endpoint, name, folder=folder).read_text(),
    )
    return content if isinstance(content, list) else [content]


def page_models[T: GAPIBaseModel](
    endpoint: BaseEndpoint[T],
    name: str,
    *,
    folder: str | None = None,
) -> list[T]:
    """Recorded page(s) as a list of parsed models, wrapping a single page."""
    return [endpoint.parse(page) for page in page_dicts(endpoint, name, folder=folder)]


def download_and_save(
    endpoint: GAPIClient[Any],
    name: str,
    get: Callable[[], dict[str, Any] | list[dict[str, Any]]],
    *,
    folder: str | None = None,
) -> Path:
    json_path = get_json_path(endpoint, name, folder=folder)
    if json_path.exists():
        pytest.skip(f"File already recorded for {type(endpoint).__name__}/{name}")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(get(), indent=2))
    return json_path


def assert_error(
    endpoint: GAPIClient[Any],
    name: str,
    download: Callable[[], object],
    error: type[Exception],
) -> None:
    if get_error_path(endpoint, name).exists():
        pytest.skip(f"File already recorded for {type(endpoint).__name__}/{name}")
    with pytest.raises(error) as excinfo:
        download()
    record_error(endpoint, name, getattr(excinfo.value, "response", None))


def get_error_path(endpoint: GAPIClient[Any], name: str) -> Path:
    folder = f"Errors/{endpoint.json_files_folder().name}"
    return get_json_path(endpoint, name, folder=folder)


def record_error(
    endpoint: GAPIClient[Any],
    name: str,
    data: dict[str, Any] | None = None,
) -> None:
    json_path = get_error_path(endpoint, name)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, indent=2) if data is not None else ""
    json_path.write_text(content)
