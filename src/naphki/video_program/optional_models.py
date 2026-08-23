from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import BaseModel, ConfigDict
from typing import Any

class LandscapeItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    url: str | None = None
    width: int | None = None
    height: int | None = None

class PortraitItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    url: str | None = None
    width: int | None = None
    height: int | None = None

class Images(BaseModel):
    model_config = ConfigDict(extra='ignore')
    landscape: list[LandscapeItem] | None = None
    portrait: list[PortraitItem] | None = None

class Image(BaseModel):
    model_config = ConfigDict(extra='ignore')
    url: str | None = None
    width: int | None = None
    height: int | None = None

class Logo(BaseModel):
    model_config = ConfigDict(extra='ignore')
    url: str | None = None
    width: int | None = None

class Sp(BaseModel):
    model_config = ConfigDict(extra='ignore')
    images: list[Image] | None = None
    logo: Logo | None = None

class Pc(BaseModel):
    model_config = ConfigDict(extra='ignore')
    images: list[Image] | None = None
    logo: Logo | None = None

class Hero(BaseModel):
    model_config = ConfigDict(extra='ignore')
    sp: Sp | None = None
    pc: Pc | None = None

class Category(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str | None = None
    url: str | None = None
    name: str | None = None
    uri: str | None = None

class VideoEpisodes(BaseModel):
    model_config = ConfigDict(extra='ignore')
    total: int | None = None
    uri: str | None = None

class VideoClips(BaseModel):
    model_config = ConfigDict(extra='ignore')
    total: int | None = None
    uri: str | None = None

class Casts(BaseModel):
    model_config = ConfigDict(extra='ignore')
    title: Any | None = None
    total: int | None = None
    uri: str | None = None

class VideoProgramModel(BaseModel):
    model_config = ConfigDict(extra='ignore')
    type: str | None = None
    id: str | None = None
    lang: str | None = None
    langs: list[str] | None = None
    url: str | None = None
    external_url: Any | None = None
    title: str | None = None
    html_title: str | None = None
    description: str | None = None
    html_description: str | None = None
    series_id: str | None = None
    sort_key: str | None = None
    is_new: bool | None = None
    is_closed: bool | None = None
    episode_sort: str | None = None
    sns_image: str | None = None
    images: Images | None = None
    hero: Hero | None = None
    banners: list[Any] | None = None
    categories: list[Category] | None = None
    tags: list[Any] | None = None
    video_episodes: VideoEpisodes | None = None
    video_clips: VideoClips | None = None
    casts: Casts | None = None
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
