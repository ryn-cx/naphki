# TODO: Validate
# ruff: noqa: D100, D101, D102, TC001, TC002, TC003
from typing import Any

from good_ass_pydantic_integrator import GAPIBaseModel
from pydantic import AwareDatetime, ConfigDict


class LandscapeItem(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    width: int
    height: int


class PortraitItem(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    width: int
    height: int


class Images(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    landscape: list[LandscapeItem]
    portrait: list[PortraitItem]


class Image(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    width: int
    height: int


class Logo(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    width: int


class Sp(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    images: list[Image]
    logo: Logo


class Pc(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    images: list[Image]
    logo: Logo


class Hero(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    sp: Sp
    pc: Pc


class Category(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    url: str
    name: str
    uri: str


class VideoEpisodes(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    total: int
    uri: str


class VideoClips(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    total: int
    uri: str


class Casts(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    title: None
    total: int
    uri: str


class Nahpki(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    timestamp: AwareDatetime
    params: dict[str, Any]


class Naphki(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    timestamp: AwareDatetime
    params: dict[str, Any]


class VideoProgramsModel(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
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
    nahpki: Nahpki | None = None
    naphki: Naphki | None = None
