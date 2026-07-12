# TODO: Validate
# ruff: noqa: D100, D101, D102, TC001, TC002, TC003
from typing import Any

from good_ass_pydantic_integrator import GAPIBaseModel
from pydantic import AwareDatetime, ConfigDict, Field


class FieldShards(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    total: int
    successful: int
    skipped: int
    failed: int


class Total(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    value: int
    relation: str


class FieldSource(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    thumbnail: str
    description: str
    title: str
    url: str
    slug: str


class Hit(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    field_index: str = Field(..., alias="_index")
    field_id: str = Field(..., alias="_id")
    field_score: float = Field(..., alias="_score")
    field_source: FieldSource = Field(..., alias="_source")


class Hits(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    total: Total
    max_score: float
    hits: list[Hit]


class MultiMatch(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str
    type: str
    fields: list[str]
    operator: str


class ShouldItem(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    multi_match: MultiMatch


class Bool(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    should: list[ShouldItem]


class Query(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    bool: Bool


class Body(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    query: Query
    from_: int = Field(..., alias="from")
    size: int
    field_source: list[str] = Field(..., alias="_source")


class Nahpki(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    timestamp: AwareDatetime
    params: dict[str, Any]
    body: Body


class ShouldItem1(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    multi_match: MultiMatch


class Bool1(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    should: list[ShouldItem1]


class Query1(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    bool: Bool1


class Body1(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    query: Query1
    from_: int = Field(..., alias="from")
    size: int
    field_source: list[str] = Field(..., alias="_source")


class Naphki(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    timestamp: AwareDatetime
    params: dict[str, Any]
    body: Body1


class ShowsSearchModel(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    took: int
    timed_out: bool
    field_shards: FieldShards = Field(..., alias="_shards")
    hits: Hits
    nahpki: Nahpki | None = None
    naphki: Naphki | None = None
