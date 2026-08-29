from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import ConfigDict
from pydantic import AwareDatetime, BaseModel

class Pagination(BaseModel):
    model_config = ConfigDict(defer_build=True)
    limit: int
    offset: int
    count: int
    total: int
    next: str | None
    previous: None

class VideoProgram(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: str
    title: str
    html_title: str
    url: str
    uri: str

class BroadcastSchedule(BaseModel):
    model_config = ConfigDict(defer_build=True)
    start_at: AwareDatetime
    end_at: AwareDatetime

class Image(BaseModel):
    model_config = ConfigDict(defer_build=True)
    url: str
    width: int
    height: int

class Video(BaseModel):
    model_config = ConfigDict(defer_build=True)
    vod_id: None
    url: str
    duration: int
    analytics: str
    published_at: AwareDatetime
    expired_at: AwareDatetime

class Category(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: str
    url: str
    name: str
    uri: str

class Tag(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: str
    url: str
    name: str
    uri: str

class Item(BaseModel):
    model_config = ConfigDict(defer_build=True)
    type: str
    id: str
    lang: str
    caption_langs: list[str]
    voice_langs: list[str]
    video_program: VideoProgram
    url: str
    title: str | None
    html_title: str | None
    description: str
    html_description: str
    broadcast_schedules: list[BroadcastSchedule]
    first_broadcasted_at: AwareDatetime
    images: list[Image]
    video: Video
    categories: list[Category]
    tags: list[Tag]

class VideoEpisodesModel(BaseModel):
    model_config = ConfigDict(defer_build=True)
    pagination: Pagination
    items: list[Item]
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
