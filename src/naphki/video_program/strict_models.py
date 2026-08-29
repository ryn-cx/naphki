from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import ConfigDict
from pydantic import BaseModel

class LandscapeItem(BaseModel):
    model_config = ConfigDict(defer_build=True)
    url: str
    width: int
    height: int

class PortraitItem(BaseModel):
    model_config = ConfigDict(defer_build=True)
    url: str
    width: int
    height: int

class Images(BaseModel):
    model_config = ConfigDict(defer_build=True)
    landscape: list[LandscapeItem]
    portrait: list[PortraitItem]

class Image(BaseModel):
    model_config = ConfigDict(defer_build=True)
    url: str
    width: int
    height: int

class Logo(BaseModel):
    model_config = ConfigDict(defer_build=True)
    url: str
    width: int

class Sp(BaseModel):
    model_config = ConfigDict(defer_build=True)
    images: list[Image]
    logo: Logo

class Pc(BaseModel):
    model_config = ConfigDict(defer_build=True)
    images: list[Image]
    logo: Logo

class Hero(BaseModel):
    model_config = ConfigDict(defer_build=True)
    sp: Sp
    pc: Pc

class Sp1(BaseModel):
    model_config = ConfigDict(defer_build=True)
    url: str
    width: int
    height: int

class Pc1(BaseModel):
    model_config = ConfigDict(defer_build=True)
    url: str
    width: int
    height: int

class Image2(BaseModel):
    model_config = ConfigDict(defer_build=True)
    sp: Sp1
    pc: Pc1
    alt: str

class Banner(BaseModel):
    model_config = ConfigDict(defer_build=True)
    url: str
    image: Image2

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

class VideoEpisodes(BaseModel):
    model_config = ConfigDict(defer_build=True)
    total: int
    uri: str

class VideoClips(BaseModel):
    model_config = ConfigDict(defer_build=True)
    total: int
    uri: str

class Casts(BaseModel):
    model_config = ConfigDict(defer_build=True)
    title: None
    total: int
    uri: str

class VideoProgramModel(BaseModel):
    model_config = ConfigDict(defer_build=True)
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
    banners: list[Banner]
    categories: list[Category]
    tags: list[Tag]
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
