from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import BaseModel
from typing import Any

class LandscapeItem(BaseModel):
    url: str
    width: int
    height: int

class PortraitItem(BaseModel):
    url: str
    width: int
    height: int

class Images(BaseModel):
    landscape: list[LandscapeItem]
    portrait: list[PortraitItem]

class Image(BaseModel):
    url: str
    width: int
    height: int

class Logo(BaseModel):
    url: str
    width: int

class Sp(BaseModel):
    images: list[Image]
    logo: Logo

class Pc(BaseModel):
    images: list[Image]
    logo: Logo

class Hero(BaseModel):
    sp: Sp
    pc: Pc

class Category(BaseModel):
    id: str
    url: str
    name: str
    uri: str

class VideoEpisodes(BaseModel):
    total: int
    uri: str

class VideoClips(BaseModel):
    total: int
    uri: str

class Casts(BaseModel):
    title: None
    total: int
    uri: str

class VideoProgramModel(BaseModel):
    type: str
    id: str
    lang: str
    langs: list[str]
    url: str
    external_url: None
    title: str
    html_title: str
    description: str
    html_description: str
    series_id: str
    sort_key: str
    is_new: bool
    is_closed: bool
    episode_sort: str
    sns_image: str
    images: Images
    hero: Hero
    banners: list[None]
    categories: list[Category]
    tags: list[None]
    video_episodes: VideoEpisodes
    video_clips: VideoClips
    casts: Casts
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
