from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import AwareDatetime, BaseModel
from typing import Any

class Pagination(BaseModel):
    limit: int
    offset: int
    count: int
    total: int
    next: str | None
    previous: None

class VideoProgram(BaseModel):
    id: str
    title: str
    html_title: str
    url: str
    uri: str

class BroadcastSchedule(BaseModel):
    start_at: AwareDatetime
    end_at: AwareDatetime

class Image(BaseModel):
    url: str
    width: int
    height: int

class Video(BaseModel):
    vod_id: None
    url: str
    duration: int
    analytics: str
    published_at: AwareDatetime
    expired_at: AwareDatetime

class Category(BaseModel):
    id: str
    url: str
    name: str
    uri: str

class Item(BaseModel):
    type: str
    id: str
    lang: str
    caption_langs: list[None]
    voice_langs: list[str]
    video_program: VideoProgram
    url: str
    title: str
    html_title: str
    description: str
    html_description: str
    broadcast_schedules: list[BroadcastSchedule]
    first_broadcasted_at: AwareDatetime
    images: list[Image]
    video: Video
    categories: list[Category]
    tags: list[None]

class VideoEpisodesModel(BaseModel):
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
