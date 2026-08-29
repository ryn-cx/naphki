from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import BaseModel, ConfigDict, Field

class FieldShards(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    total: int | None = None
    successful: int | None = None
    skipped: int | None = None
    failed: int | None = None

class Total(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    value: int | None = None
    relation: str | None = None

class FieldSource(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    thumbnail: str | None = None
    description: str | None = None
    title: str | None = None
    url: str | None = None
    slug: str | None = None

class Hit(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    field_index: str | None = Field(None, alias='_index')
    field_id: str | None = Field(None, alias='_id')
    field_score: float | None = Field(None, alias='_score')
    field_source: FieldSource | None = Field(None, alias='_source')

class Hits(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    total: Total | None = None
    max_score: float | None = None
    hits: list[Hit] | None = None

class ShowsSearchModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    took: int | None = None
    timed_out: bool | None = None
    field_shards: FieldShards | None = Field(None, alias='_shards')
    hits: Hits | None = None
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
