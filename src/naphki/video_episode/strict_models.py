from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import ConfigDict
from pydantic import AwareDatetime, BaseModel
from typing import Any

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

class Image1(BaseModel):
    model_config = ConfigDict(defer_build=True)
    url: str
    width: int
    height: int
    caption: str
    html_caption: str

class Content(BaseModel):
    model_config = ConfigDict(defer_build=True)
    title: None
    html_title: None
    image: Image1
    body: None
    html_body: None

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

class RelatedVideos(BaseModel):
    model_config = ConfigDict(defer_build=True)
    total: int
    uri: str

class VideoEpisodeModel(BaseModel):
    model_config = ConfigDict(defer_build=True)
    type: str
    id: str
    lang: str
    caption_langs: list[None]
    voice_langs: list[str]
    video_program: VideoProgram
    url: str
    title: None
    html_title: None
    description: str
    html_description: str
    broadcast_schedules: list[BroadcastSchedule]
    first_broadcasted_at: AwareDatetime
    sns_image: str
    images: list[Image]
    video: Video
    contents: list[Content]
    categories: list[Category]
    tags: list[Tag]
    related_videos: RelatedVideos
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
