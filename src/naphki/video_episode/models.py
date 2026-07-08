# ruff: noqa: D100, D101, D102, TC001, TC002, TC003
from good_ass_pydantic_integrator import GAPIBaseModel
from pydantic import AwareDatetime, ConfigDict


class VideoProgram(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    html_title: str
    url: str
    uri: str


class BroadcastSchedule(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    start_at: AwareDatetime
    end_at: AwareDatetime


class Image(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    width: int
    height: int


class Video(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    vod_id: None
    url: str
    duration: int
    analytics: str
    published_at: AwareDatetime
    expired_at: AwareDatetime


class Image1(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    width: int
    height: int
    caption: str
    html_caption: str


class Content(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    title: None
    html_title: None
    image: Image1
    body: None
    html_body: None


class Category(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    url: str
    name: str
    uri: str


class Tag(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    url: str
    name: str
    uri: str


class RelatedVideos(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    total: int
    uri: str


class Params(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    schedule: bool


class Naphki(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    timestamp: AwareDatetime
    params: Params


class VideoEpisodeModel(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
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
    naphki: Naphki
