from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from typing import Any
from pydantic import AwareDatetime, BaseModel, ConfigDict

class Pagination(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    limit: int | None = None
    offset: int | None = None
    count: int | None = None
    total: int | None = None
    next: str | None = None
    previous: Any | None = None

class VideoProgram(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    id: str | None = None
    title: str | None = None
    html_title: str | None = None
    url: str | None = None
    uri: str | None = None

class BroadcastSchedule(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    start_at: AwareDatetime | None = None
    end_at: AwareDatetime | None = None

class Image(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    url: str | None = None
    width: int | None = None
    height: int | None = None

class Video(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    vod_id: Any | None = None
    url: str | None = None
    duration: int | None = None
    analytics: str | None = None
    published_at: AwareDatetime | None = None
    expired_at: AwareDatetime | None = None

class Category(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    id: str | None = None
    url: str | None = None
    name: str | None = None
    uri: str | None = None

class Item(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    type: str | None = None
    id: str | None = None
    lang: str | None = None
    caption_langs: list[Any] | None = None
    voice_langs: list[str] | None = None
    video_program: VideoProgram | None = None
    url: str | None = None
    title: str | None = None
    html_title: str | None = None
    description: str | None = None
    html_description: str | None = None
    broadcast_schedules: list[BroadcastSchedule] | None = None
    first_broadcasted_at: AwareDatetime | None = None
    images: list[Image] | None = None
    video: Video | None = None
    categories: list[Category] | None = None
    tags: list[Any] | None = None

class VideoEpisodesModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    pagination: Pagination | None = None
    items: list[Item] | None = None
    _raw_input: Any = PrivateAttr(default=None)

    @model_validator(mode='wrap')
    @classmethod
    def _capture_raw_input(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        """Validate the model and keep the input it was built from."""
        model = handler(data)
        model._raw_input = data
        return model

    @property
    def raw_input(self) -> Any:
        """The input this model was validated from, as it was handed over."""
        return self._raw_input
