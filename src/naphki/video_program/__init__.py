# TODO: Validate
"""Contains the VideoProgram class."""

from __future__ import annotations

import json
from http import HTTPStatus
from logging import NullHandler, getLogger

from naphki.base_api_endpoint import BaseEndpoint
from naphki.exceptions import ProgramNotFoundError, ResourceNotFoundError
from naphki.video_program.models import VideoProgramModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())


# TODO: Validate
class VideoProgram(BaseEndpoint):
    """Manage the video program file.

    Source: https://www3.nhk.or.jp/nhkworld/en/shows/{program_id}/

    Example request:
        - GET /showsapi/v1/en/video_programs/{program_id}
            - HTTP/2
        - Host: api.nhkworld.jp
        - User-Agent: __REDACTED__
        - Accept: application/json
        - Accept-Language: en-US,en;q=0.9
        - Accept-Encoding: gzip, deflate, br, zstd
        - Connection: keep-alive
        - Referer: https://www3.nhk.or.jp/nhkworld/en/shows/{program_id}/
        - Sec-Fetch-Dest: empty
        - Sec-Fetch-Mode: cors
        - Sec-Fetch-Site: cross-site
    """

    # TODO: Validate
    def __call__(self, program_id: str, language: str = "") -> VideoProgramModel:
        """Look the show up and return the model it is read into."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(self.download(program_id, language), log_id)

    # TODO: Validate
    def download(self, program_id: str, language: str = "") -> str:
        """Download the video program file."""
        log_id = self.get_log_id(self.download, locals())
        resolved_language = language or self._client.language
        try:
            response = self._client.download(
                endpoint=f"showsapi/v1/{resolved_language}/video_programs/{program_id}",
                params={},
                log_id=log_id,
            )
        except ResourceNotFoundError as err:
            raise ProgramNotFoundError(
                program_id,
                err.status_code,
                err.response,
            ) from err
        return self._validate_download(response, program_id)

    # TODO: Validate
    def _validate_download(self, response: str, program_id: str) -> str:
        if json.loads(response).get("id") != program_id:
            raise ProgramNotFoundError(program_id, HTTPStatus.OK, response)
        return response

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> VideoProgramModel:
        """Read a downloaded video program file into its model."""
        return model_validate_json(data, log_id or self.default_log_id)
