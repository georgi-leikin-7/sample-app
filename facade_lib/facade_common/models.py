from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel, to_pascal


class InvocationPayloadModel(BaseModel):

    model_config = ConfigDict(extra="forbid")

    endpoint: str
    body: str | None = Field(default=None)


class InvocationRequestModel(BaseModel):

    model_config = ConfigDict(extra="ignore", alias_generator=to_pascal, populate_by_name=True)

    function_name: str
    invocation_type: str
    payload: str


class LambdaResponseHeadersModel(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    content_type: str = Field(alias="Content-Type", default="application/json")
    content_disposition: Optional[str] = Field(alias="Content-Disposition", default=None)


class LambdaResponseModel(BaseModel):

    model_config = ConfigDict(alias_generator=to_camel, extra="allow", populate_by_name=True)

    is_base_64_encoded: bool
    status_code: int
    headers: dict
    body: Optional[str] = Field(default=None)
