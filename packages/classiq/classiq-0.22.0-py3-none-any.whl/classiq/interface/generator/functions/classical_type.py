from typing import Union

import pydantic
from pydantic import Field
from typing_extensions import Annotated, Literal

from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)


class Integer(HashablePydanticBaseModel):
    kind: Literal["int"] = pydantic.Field(default="int")


class Real(HashablePydanticBaseModel):
    kind: Literal["real"] = pydantic.Field(default="real")


class Bool(HashablePydanticBaseModel):
    kind: Literal["bool"] = pydantic.Field(default="bool")


class ClassicalList(HashablePydanticBaseModel):
    kind: Literal["list"] = pydantic.Field(default="list")
    element_type: "ClassicalType"


ClassicalType = Annotated[
    Union[Integer, Real, Bool, ClassicalList], Field(discriminator="kind")
]
ClassicalList.update_forward_refs()
