"""VideoProgramModel, strict to a type checker, all-optional at runtime.

A type checker reads the strict model, so every field carries the type and
the requiredness the schema recorded. At runtime the all-optional copy is imported
instead, so a response that has drifted still parses and a field the data is
missing is None despite what its type hint says.
"""

from typing import TYPE_CHECKING

from good_ass_pydantic_integrator import load

from .optional_models import VideoProgramModel as OptionalModel
from .strict_models import VideoProgramModel as StrictModel

if TYPE_CHECKING:
    from .strict_models import (
        Banner,
        Casts,
        Category,
        Hero,
        Image,
        Image2,
        Images,
        LandscapeItem,
        Logo,
        Pc,
        Pc1,
        PortraitItem,
        Sp,
        Sp1,
        Tag,
        VideoClips,
        VideoEpisodes,
        VideoProgramModel,
    )
else:
    from .optional_models import (
        Banner,
        Casts,
        Category,
        Hero,
        Image,
        Image2,
        Images,
        LandscapeItem,
        Logo,
        Pc,
        Pc1,
        PortraitItem,
        Sp,
        Sp1,
        Tag,
        VideoClips,
        VideoEpisodes,
        VideoProgramModel,
    )

__all__ = [
    "Banner",
    "Casts",
    "Category",
    "Hero",
    "Image",
    "Image2",
    "Images",
    "LandscapeItem",
    "Logo",
    "Pc",
    "Pc1",
    "PortraitItem",
    "Sp",
    "Sp1",
    "Tag",
    "VideoClips",
    "VideoEpisodes",
    "VideoProgramModel",
    "model_validate_json",
]


def model_validate_json(data: str | bytes | object, log_id: str) -> VideoProgramModel:
    """Read a downloaded file into VideoProgramModel."""
    return load.model_validate_json(StrictModel, OptionalModel, data, log_id)
