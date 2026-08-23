from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import AwareDatetime, BaseModel, ConfigDict
from typing import Any

class VideoProgram(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str | None = None
    title: str | None = None
    html_title: str | None = None
    url: str | None = None
    uri: str | None = None

class BroadcastSchedule(BaseModel):
    model_config = ConfigDict(extra='ignore')
    start_at: AwareDatetime | None = None
    end_at: AwareDatetime | None = None

class Image(BaseModel):
    model_config = ConfigDict(extra='ignore')
    url: str | None = None
    width: int | None = None
    height: int | None = None

class Video(BaseModel):
    model_config = ConfigDict(extra='ignore')
    vod_id: Any | None = None
    url: str | None = None
    duration: int | None = None
    analytics: str | None = None
    published_at: AwareDatetime | None = None
    expired_at: AwareDatetime | None = None

class Image1(BaseModel):
    model_config = ConfigDict(extra='ignore')
    url: str | None = None
    width: int | None = None
    height: int | None = None
    caption: str | None = None
    html_caption: str | None = None

class Content(BaseModel):
    model_config = ConfigDict(extra='ignore')
    title: Any | None = None
    html_title: Any | None = None
    image: Image1 | None = None
    body: Any | None = None
    html_body: Any | None = None

class Category(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str | None = None
    url: str | None = None
    name: str | None = None
    uri: str | None = None

class Tag(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str | None = None
    url: str | None = None
    name: str | None = None
    uri: str | None = None

class RelatedVideos(BaseModel):
    model_config = ConfigDict(extra='ignore')
    total: int | None = None
    uri: str | None = None

class VideoEpisodeModel(BaseModel):
    model_config = ConfigDict(extra='ignore')
    type: str | None = None
    id: str | None = None
    lang: str | None = None
    caption_langs: list[Any] | None = None
    voice_langs: list[str] | None = None
    video_program: VideoProgram | None = None
    url: str | None = None
    title: Any | None = None
    html_title: Any | None = None
    description: str | None = None
    html_description: str | None = None
    broadcast_schedules: list[BroadcastSchedule] | None = None
    first_broadcasted_at: AwareDatetime | None = None
    sns_image: str | None = None
    images: list[Image] | None = None
    video: Video | None = None
    contents: list[Content] | None = None
    categories: list[Category] | None = None
    tags: list[Tag] | None = None
    related_videos: RelatedVideos | None = None
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
