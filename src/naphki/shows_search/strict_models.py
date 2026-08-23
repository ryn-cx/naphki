from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import BaseModel, Field

class FieldShards(BaseModel):
    total: int
    successful: int
    skipped: int
    failed: int

class Total(BaseModel):
    value: int
    relation: str

class FieldSource(BaseModel):
    thumbnail: str
    description: str
    title: str
    url: str
    slug: str

class Hit(BaseModel):
    field_index: str = Field(..., alias='_index')
    field_id: str = Field(..., alias='_id')
    field_score: float = Field(..., alias='_score')
    field_source: FieldSource = Field(..., alias='_source')

class Hits(BaseModel):
    total: Total
    max_score: float | None
    hits: list[Hit]

class ShowsSearchModel(BaseModel):
    took: int
    timed_out: bool
    field_shards: FieldShards = Field(..., alias='_shards')
    hits: Hits
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
